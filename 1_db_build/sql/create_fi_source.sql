CREATE TABLE fi.source (
	source_code varchar(6) PRIMARY KEY
  , source_text varchar(80)
  , display_level int4
  , selectable varchar(1)
  , sort_sequence int4
  , extra varchar(255)
);