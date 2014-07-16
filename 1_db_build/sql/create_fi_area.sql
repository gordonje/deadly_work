CREATE TABLE fi.area (
	area_code varchar(3) PRIMARY KEY
  , area_text varchar(80)
  , display_level int4
  , selectable varchar(1)
  , sort_sequence int4
  , extra varchar(255)
);