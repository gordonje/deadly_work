import os
import getpass
import psycopg2
import requests

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

def get_time_series_file(series_name, series_file):

	print "Getting %(series)s %(file_name)s..." % {"series": series_name, "file_name": series_file}

	text_file = series_name + '_' + series_file + '.txt'

	if os.path.isfile(text_file):
		print "    Found local file..."
	else:
		print "    Downloading..."

		if "Current" in series_file:
			url = "http://download.bls.gov/pub/time.series/" + series_name + "/" + series_name + ".data.0." + series_file
		elif "AllData" in series_file:
			url = "http://download.bls.gov/pub/time.series/" + series_name + "/" + series_name + ".data.1." + series_file
		else:
			url = "http://download.bls.gov/pub/time.series/" + series_name + "/" + series_name + "." + series_file

		with open(text_file, 'w') as out_file:

			response = session.get(url)

			out_file.write(response.content.split('\n', 1)[1])

		out_file.closed

	return os.getcwd() + '/' + text_file

def make_table(conn_string, sql_file):

	print "    Making table..."

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(open(sql_file, "r").read())

def import_file(conn_string, schema_name, table_name, text_file_w_path):

	print "    Importing data..."

	copy_from_sql = "COPY %(schema)s.%(table)s FROM '%(file)s' WITH (DELIMITER E'\t');" % {'schema': schema_name, 'table': table_name, 'file': text_file_w_path}

	with psycopg2.connect(conn_string) as conn:
		with conn.cursor() as cur:
			cur.execute(copy_from_sql)

def handle_file(conn_string, series_name, file_name):

	if has_table(conn_string, series_name, file_name.lower()) == False:
	
		file_w_path = get_time_series_file(series_name, file_name)

		make_table(conn_string, "sql/create_%(schema)s_%(table)s.sql" % {"schema": series_name, "table": file_name})

		import_file(conn_string, series_name, file_name, file_w_path)
	else:
		print 'Already have %(series)s %(file)s...' % {"series": series_name, "file": file_name}



db = raw_input("Enter name of target database):")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}

session = requests.Session()
session.headers.update({"Connection": "keep-alive"})

# Make the fw schema if it doesn't already exist
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute('''CREATE SCHEMA IF NOT EXISTS fw;''')

handle_file(conn_string, 'fw', 'AllData')

handle_file(conn_string, 'fw', 'area')

handle_file(conn_string, 'fw', 'case')

handle_file(conn_string, 'fw', 'category')

handle_file(conn_string, 'fw', 'category2')

handle_file(conn_string, 'fw', 'Current')

handle_file(conn_string, 'fw', 'event')

handle_file(conn_string, 'fw', 'industry')

handle_file(conn_string, 'fw', 'occupation')

handle_file(conn_string, 'fw', 'series')

handle_file(conn_string, 'fw', 'source')


# Make the fi schema if it doesn't already exist
with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute('''CREATE SCHEMA IF NOT EXISTS fi;''')

handle_file(conn_string, 'fi', 'AllData')

handle_file(conn_string, 'fi', 'area')

handle_file(conn_string, 'fi', 'case')

handle_file(conn_string, 'fi', 'category')

handle_file(conn_string, 'fi', 'category2')

handle_file(conn_string, 'fi', 'Current')

handle_file(conn_string, 'fi', 'event')

handle_file(conn_string, 'fi', 'industry')

handle_file(conn_string, 'fi', 'occupation')

handle_file(conn_string, 'fi', 'series')

handle_file(conn_string, 'fi', 'source')


if has_table(conn_string, 'public', 'cfoi_data') == False:

	print "Combining CFOI data..."

	make_table(conn_string, 'sql/combine_cfoi_data.sql')


cur.close()
conn.close()

print "Finished."