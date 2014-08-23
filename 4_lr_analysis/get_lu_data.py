import getpass
import psycopg2
import requests

db = raw_input("Enter name of target database:")
user = raw_input("Enter your PostgreSQL username (this might just be 'postgres'):")
password = getpass.getpass("Enter your PostgreSQL user password:")

conn = psycopg2.connect("dbname=%(db)s user=%(user)s password=%(password)s" % {"db": db, "user": user, "password":password})
cur = conn.cursor()

session = requests.Session()
session.headers.update({"Connection": "keep-alive"})

# create the schema if it doesn't already exist

cur.execute('''CREATE SCHEMA IF NOT EXISTS lu;''')
conn.commit()

# if the current data table doesn't already exist, create and populate it

cur.execute('''SELECT * FROM information_schema.tables WHERE table_name = 'current_data' AND table_schema = 'lu';''')
has_current_data = cur.fetchone()

if has_current_data == None:

    print "Getting current data..."

    cur.execute('''CREATE TABLE lu.current_data (
                    series_id varchar(17) 
                    , year int4
                    , period varchar(3)
                    , value numeric
                    , footnote_codes varchar(255)
                    , PRIMARY KEY (series_id, year)
                    );''')
    conn.commit()

    response = session.get("http://download.bls.gov/pub/time.series/lu/lu.data.0.Current")
    rows = response.content.split('\n')

    for row in rows[1:]:
        values = row.split('\t')

        if len(values) > 1:
            cur.execute('''INSERT INTO lu.current_data (series_id, year, period, value, footnote_codes) 
                            VALUES (%s, %s, %s, %s, %s);''', 
                            [values[0].strip(), values[1].strip(), values[2].strip(), values[3].strip(), values[4].strip()])
            conn.commit()


# if the all data table doesn't already exist, create and populate it

cur.execute('''SELECT * FROM information_schema.tables WHERE table_name = 'all_data' AND table_schema = 'lu';''')
has_all_data = cur.fetchone()

if has_all_data == None:

    print "Getting all data..."

    cur.execute('''CREATE TABLE lu.all_data (
                    series_id varchar(17) 
                    , year int4
                    , period varchar(3)
                    , value numeric
                    , footnote_codes varchar(255)
                    , PRIMARY KEY (series_id, year)
                    );''')
    conn.commit()

    response = session.get("http://download.bls.gov/pub/time.series/lu/lu.data.1.AllData")
    rows = response.content.split('\n')

    for row in rows[1:]:
        values = row.split('\t')

        if len(values) > 1:
            cur.execute('''INSERT INTO lu.all_data (series_id, year, period, value, footnote_codes) 
                            VALUES (%s, %s, %s, %s, %s);''', 
                            [values[0].strip(), values[1].strip(), values[2].strip(), values[3].strip(), values[4].strip()])
            conn.commit()


# if the series table doesn't already exist, create and populate it

cur.execute('''SELECT * FROM information_schema.tables WHERE table_name = 'series' AND table_schema = 'lu';''')
has_series = cur.fetchone()

if has_series == None:

	print "Getting series..."

	cur.execute('''CREATE TABLE lu.series (
                    series_id varchar(17) PRIMARY KEY
                  , lfst_code varchar(2)
                  , fips_code varchar(2)
                  , series_description varchar(255)
                  , tdata_code varchar(2)
                  , pcts_code varchar(2)
                  , earn_code varchar(2)
                  , class_code varchar(2)
                  , unin_code varchar(1)
                  , indy_code varchar(4)
                  , occupation_code varchar(4)
                  , education_code varchar(2)
                  , ages_code varchar(2)
                  , race_code varchar(2)
                  , orig_code varchar(2)
                  , sexs_code varchar(2)
                  , seasonal varchar(2)
                  , footnote_codes varchar(255)
                  , begin_year int4
                  , begin_period varchar(3)
                  , end_year int4
                  , end_period varchar(3)
                    );''')
	conn.commit()

	response = session.get("http://download.bls.gov/pub/time.series/lu/lu.series")
	rows = response.content.split('\n')

	for row in rows[1:]:
		values = row.split('\t')

		if len(values) > 1:
			cur.execute('''INSERT INTO lu.series (series_id, lfst_code, fips_code, series_description, tdata_code, pcts_code, earn_code, 
												class_code, unin_code, indy_code, occupation_code, education_code, ages_code, race_code, 
												orig_code, sexs_code, seasonal, footnote_codes, begin_year, begin_period, end_year, end_period) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);''', 
                            [values[0].strip(), values[1].strip(), values[2].strip(), values[3].strip(), values[4].strip(),
                             values[5].strip(), values[6].strip(), values[7].strip(), values[8].strip(), values[9].strip(),
                             values[10].strip(), values[11].strip(), values[12].strip(), values[13].strip(), values[14].strip(),
                             values[15].strip(), values[16].strip(), values[17].strip(), values[18].strip(), values[19].strip(),
                             values[20].strip(), values[21].strip()])
			conn.commit()


# check to see if the columns are on the areas table, then add them.  


cur.close()
conn.close()