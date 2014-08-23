import psycopg2
import getpass
import csv
import re

user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn = psycopg2.connect("dbname=bls user=%(user)s password=%(password)s" % {"user": user, "password":password})
cur = conn.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS public.governors (
                  year int4 
                , state varchar(20)
                , governor varchar(80)
                , party varchar(20)
                );''')
conn.commit()

with open('governors.csv', 'rb') as in_file:
	file_reader = csv.DictReader(in_file, dialect='excel')
	for row in file_reader:

		guv_split = row['Governor'].split('(')

		name = guv_split[0].strip()

		if len(guv_split) == 2:
			party = guv_split[1].rstrip(')').strip()
		else:
			party = None

		cur.execute('''INSERT INTO public.governors (year, state, governor, party)
						VALUES (%s, %s, %s, %s);''', (row['Year'], row['State'], name, party))
		conn.commit()

in_file.close()

print "Finished."

cur.close()
conn.close()
