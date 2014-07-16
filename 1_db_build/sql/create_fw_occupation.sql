CREATE TABLE fw.occupation (
	occupation_code varchar(6) PRIMARY KEY
  , occupation_text varchar(255)
  , display_level int4
  , selectable varchar(1)
  , sort_sequence int4
  , extra varchar(255)
);