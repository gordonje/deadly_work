import getpass
import psycopg2
import json

def query_db(conn_string, sql_string, parameter_tuple = ()):

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(sql_string, parameter_tuple)
			return cur.fetchall()


db =  raw_input("Enter name of target database:")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}

states = []

states_query = '''SELECT
					  a.state_code
					, a.state_name
					, a.emplvl_total::int
					, a.fatals_total::int
					, b.is_right_to_work
					, ROUND(b.pct_union_repd_avg, 1)
				FROM states_naics2_no_agri a
				JOIN areas b
				ON a.state_code = LEFT(b.cew_code, 2)
				ORDER BY a.state_name;'''

for i in query_db(conn_string, states_query):
	states.append(
		{
			'state_code': i[0], 
			'state': i[1],
			'facts': {
				  'emplvl': i[2]
				, 'fatals': i[3]
				, 'is_rtw': i[4]
				, 'pct_union': str(i[5])
			},
			'sectors': []
		}
	)

output = []

for state in states:

	sector_query = '''SELECT 
							  a.cew_code
							, a.cfoi_name
							, ROUND(b.residual)::int
						FROM industries a
						JOIN states_industries b
						ON a.cew_code = b.industry_code
						WHERE a.display_level = 3 
						AND a.cew_code NOT LIKE '1%%'
						AND b.state_code = %s 
						AND b.residual IS NOT NULL
						ORDER BY b.residual DESC;'''

	for i in query_db(conn_string, sector_query, (state['state_code'],)):

		sector = {				
					'naics_code': i[0],
					'sector': i[1], 
					'residual': i[2],
					'industries': []
				}

		if '-' in sector['naics_code']:
			query_params = (state['state_code'], sector['naics_code'].split('-')[0] + '%', sector['naics_code'].split('-')[1] + '%')
		else:
			query_params = (state['state_code'], sector['naics_code'] + '%', sector['naics_code'] + '%')

		industry_query = '''SELECT 
								  a.cew_code
								, a.cfoi_name
								, ROUND((b.residual / b.expect_fatals) * 100, 1)
							FROM industries a
							JOIN states_industries b
							ON a.cew_code = b.industry_code
							WHERE a.display_level = 5 
							AND b.state_code = %s 
							AND (b.industry_code LIKE %s OR b.industry_code LIKE %s)
							AND b.residual IS NOT NULL
							AND b.expect_fatals > 0
							ORDER BY b.residual / b.expect_fatals DESC
							LIMIT 5;'''

		for j in query_db(conn_string, industry_query, query_params):

			sector['industries'].append({
					  'naics_code': j[0]
					, 'industry': j[1]
					, 'pct_oe': str(j[2])
				})

		state['sectors'].append(sector)

	output.append(state)
		

json_file = open('states_industries.json', 'w')
json_file.write(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))
json_file.close()