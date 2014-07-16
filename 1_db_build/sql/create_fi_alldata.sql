CREATE TABLE fi.alldata (
	series_id varchar(17) 
  , year int4
  , period varchar(3)
  , value int4
  , footnote_codes varchar(255)
  , PRIMARY KEY (series_id, year)
);