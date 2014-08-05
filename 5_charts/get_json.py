import getpass
import psycopg2
import json

def query_db(conn_string, sql_string):

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(sql_string)
			return cur.fetchall()


db =  raw_input("Enter name of target database:")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}

# get all the states and format for json

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

# loop over each state...

for state in states:

	# get non-agri sectors with residuals in that state...

	sector_query = '''SELECT 
							  a.cew_code
							, a.cfoi_name
							, ROUND(b.residual)::int
						FROM industries a
						JOIN states_industries b
						ON a.cew_code = b.industry_code
						WHERE a.display_level = 3 
						AND a.cew_code NOT LIKE '1%%'
						AND b.state_code = '%s' 
						AND b.residual IS NOT NULL
						ORDER BY b.residual DESC;''' % state['state_code']

	for i in query_db(conn_string, sector_query):

		sector = {				
					'naics_code': i[0],
					'sector': i[1], 
					'residual': i[2],
					'industries': []
				}

		# need to handle cases when sector code is a range, like '48-49'
		if '-' in sector['naics_code']:
			# split the sector code at the dash
			# get the min value and the max value
			min_code = int(sector['naics_code'].split('-')[0])
			max_code = int(sector['naics_code'].split('-')[1])

			sector_filter = ''

			# loop over all numbers in the range, adding an 'OR' condition for each
			for x in range(min_code, max_code + 1):

				sector_filter += "b.industry_code LIKE '" + str(x) + "%' OR "
		# if no dash, just add one sector filter
		else:
			sector_filter = "b.industry_code LIKE '" + sector['naics_code'] + "%'"

		industry_query = '''SELECT 
								  a.cew_code
								, a.cfoi_name
								, ROUND((b.residual / b.expect_fatals) * 100, 1)
							FROM industries a
							JOIN states_industries b
							ON a.cew_code = b.industry_code
							WHERE a.display_level = 5 
							AND b.state_code = '%(state)s' 
							AND (%(sectors)s)
							AND b.residual IS NOT NULL
							AND b.expect_fatals > 0
							ORDER BY b.residual / b.expect_fatals DESC
							LIMIT 5;''' % {'state': state['state_code'], 'sectors': sector_filter.rstrip(' OR ')}

		# append each industry to its sector
		for j in query_db(conn_string, industry_query):

			sector['industries'].append({
					  'naics_code': j[0]
					, 'industry': j[1]
					, 'pct_oe': str(j[2])
				})

		# append all the sectors with industries to the state
		state['sectors'].append(sector)
	# append the state to the output variable
	output.append(state)
		
# write to file
json_file = open('states_industries.json', 'w')
json_file.write(json.dumps(output, sort_keys=True, indent=4, separators=(',', ': ')))
json_file.close()