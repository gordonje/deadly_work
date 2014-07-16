import psycopg2
import getpass

def has_table(conn_string, schema_name, table_name):
	query = 'SELECT * FROM information_schema.tables WHERE table_schema = %s AND table_name = %s'
	data = (schema_name, table_name)

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(query, data)
			has_table = cur.fetchone()

	if has_table == None:
		return False
	else:
		return True


db = raw_input("Enter name of target database):")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}


if has_table(conn_string, 'public', 'areas') == False:
	
	print 'Joining areas...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open("sql/join_areas.sql", "r").read())
	

if has_table(conn_string, 'public', 'industries') == False:

	print 'Joining industries...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open("sql/join_industries.sql", "r").read())


if has_table(conn_string, 'public', 'states_industries_years') == False:

	print 'Joining annual fatality count and annual employee levels...'

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open("sql/join_cfoi_to_cew.sql", "r").read())

cur.close()
conn.close()

print "Finished"