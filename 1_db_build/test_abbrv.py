import psycopg2
import getpass
import os

db = raw_input("Enter name of target database):")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn_string = "dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password}


# print 'Adding state abbreviations...'

# '    Importing from text file...'

# with psycopg2.connect(conn_string) as conn:
# 	with conn.cursor() as cur:
# 		cur.execute('''CREATE TABLE state_fips_to_abbrv (
# 							  state varchar(30)
# 							, abbrv varchar(3)
# 							, FIPS varchar(3)
# 					);''')

# 		in_file = os.getcwd() + '/state_fips_to_abbrv.txt'

in_file = os.getcwd() + '/state_fips_to_abbrv.txt'

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute('''COPY state_fips_to_abbrv FROM %s WITH (DELIMITER E'\t');''', (in_file, ))

# with psycopg2.connect(conn_string) as conn:
# 	with conn.cursor() as cur:
# 		cur.execute('ALTER TABLE areas ADD COLUMN abbrv varchar(3);')

with psycopg2.connect(conn_string) as conn:
	with conn.cursor() as cur:
		cur.execute(open("sql/add_state_abbrvs.sql", "r").read())