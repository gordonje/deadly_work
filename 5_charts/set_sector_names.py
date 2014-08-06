import psycopg2
import getpass
import csv 

def execute_sql(conn_string, sql_string, parameter_tuple):

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(sql_string, parameter_tuple)


def has_column(conn_string, schema_name, table_name, column_name):
	query = '''SELECT * FROM information_schema.columns WHERE table_schema = %s AND table_name = %s AND column_name = %s'''
	data = (schema_name, table_name, column_name)

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(query, data)
			has_column = cur.fetchone()

	if has_column == None:
		return False
	else:
		return True


db =  raw_input("Enter name of target database:")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}


if has_column(conn_string, 'public', 'industries', 'display_name') == False:

	execute_sql(conn_string, "ALTER TABLE industries ADD COLUMN display_name varchar(45);", ())


with open('sector_display_names.csv', 'rU') as in_file:
	file_reader = csv.DictReader(in_file, dialect='excel')
	for row in file_reader:

		if len(row['display_name']) > 0:

			execute_sql(conn_string, 
						'''UPDATE industries 
							SET display_name = %s 
							WHERE cew_code = %s''', (row['display_name'], row['naics_code']))

in_file.close()
