CREATE TABLE fi.industry (
	industry_code varchar(6) PRIMARY KEY
  , industry_text varchar(100)
  , display_level int4
  , selectable varchar(1)
  , sort_sequence int4
  , extra varchar(255)
);