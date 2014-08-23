import psycopg2
import getpass
import os

def execute_sql(conn_string, sql_string):

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(sql_string)

	cur.close()
	conn.close()


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

	cur.close()
	conn.close()


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

	cur.close()
	conn.close()


def import_txt_file(conn_string, schema_name, table_name, text_file_w_path):

	print "    Importing data..."

	copy_from_sql = "COPY %(schema)s.%(table)s FROM '%(file)s' WITH (DELIMITER E'\t');" % {'schema': schema_name, 'table': table_name, 'file': text_file_w_path}

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(copy_from_sql)


def import_csv_file(conn_string, schema_name, table_name, csv_file_w_path):

	print "    Importing data..."

	copy_from_sql = "COPY %(schema)s.%(table)s FROM '%(file)s' CSV HEADER;" % {'schema': schema_name, 'table': table_name, 'file': text_file_w_path}

	execute_sql(conn_string, copy_from_sql)



db = raw_input("Enter name of target database:")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}



execute_sql(conn_string, "CREATE SCHEMA IF NOT EXISTS osha;")



if has_table(conn_string, 'osha', 'inspections') == False:

	print "Importing OSHA inspections..."

	execute_sql(conn_string, open("sql/create_osha_inspections.sql", "r").read())

	file_path = os.getcwd() + '/data/osha_inspection.csv'

	import_csv_file(conn_string, 'osha', 'inspections', file_path)

	execute_sql(conn_string, 'CREATE INDEX osha_inspections_naics_code ON osha.violations (naics_code);')

	execute_sql(conn_string, 'CREATE INDEX osha_inspections_open_year ON osha.violations (open_year);')

	execute_sql(conn_string, 'CREATE INDEX osha_violations_site_state ON osha.violations (site_state);')

print "Counting inspections per state..."

if has_column(conn_string, 'public', 'areas', 'insp_count'):

	print "    Adding column..."

	execute_sql(conn_string, "ALTER TABLE public.areas ADD COLUMN insp_count numeric;")

execute_sql(conn_string, open("sql/add_insp_count.sql", "r").read())



if has_table(conn_string, 'osha', 'state_plans'):

	print "Importing state OSHA plans..."

	execute_sql(conn_string, open("sql/create_state_osha_plan.sql"))

	file_path = os.getcwd() + 'state_osha_plans.txt'

	import_txt_file(conn_string, 'osha', 'state_plans', file_path)

print "Identifying states with OSHA plans..."

if has_column(conn_string, 'public', 'areas', 'has_state_osha'):

	print "    Adding has_state_osha column..."

	execute_sql(conn_string, "ALTER TABLE public.areas ADD COLUMN has_state_osha varchar(1) DEFAULT 0;")

if has_column(conn_string, 'public', 'areas', 'has_state_osha'):

	print "    Adding is_osha_public_sector_only column..."

	execute_sql(conn_string, "ALTER TABLE public.areas ADD COLUMN is_osha_public_sector_only varchar(1) DEFAULT 0;")


execute_sql(conn_string, "sql/add_has_state_osha.sql")



if has_table(conn_string, 'osha', 'inspectors'):

	print "Importing OSHA inspector numbers per state..."

	execute_sql(conn_string, open("sql/create_osha_state_inspectors.sql"))

	file_path = os.getcwd() + 'AFL_inspectors_per_state.csv'

	import_csv_file(conn_string, 'osha', 'inspectors', file_path)

print "Adding state inspector numbers..."



if has_table(conn_string, 'osha', 'violations') == False:

	print "Importing OSHA violations..."

	execute_sql(conn_string, open("sql/create_osha_violations.sql", "r").read())

	file_path = os.getcwd() + '/data/osha_violation.csv'

	import_csv_file(conn_string, 'osha', 'violations', file_path)

	execute_sql(conn_string, 'CREATE INDEX osha_violations_activity_nr ON osha.violations (activity_nr);')

	execute_sql(conn_string, 'CREATE INDEX osha_violations_citation_id ON osha.violations (citation_id);')

	execute_sql(conn_string, 'CREATE INDEX osha_violations_issuance_date ON osha.violations (issuance_date);')

	execute_sql(conn_string, 'CREATE INDEX osha_violations_final_order_date ON osha.violations (final_order_date);')





print "Finished."