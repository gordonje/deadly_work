CREATE TABLE fw.series (
    series_id varchar(17) PRIMARY KEY
  , seasonal varchar(1)
  , category_code varchar(3)
  , datatype_code varchar(1)
  , case_code varchar(1)
  , industry_code varchar(6)
  , event_code varchar(6)
  , source_code varchar(6)
  , occupation_code varchar(6)
  , area_code varchar(3)
  , footnote_codes varchar(255)
  , begin_year int4
  , begin_period varchar(3)
  , end_year int4
  , end_period varchar(3)
);