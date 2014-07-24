CREATE TABLE fw.event (
	event_code varchar(6) PRIMARY KEY
  , event_text varchar(100)
  , display_level int4
  , selectable varchar(1)
  , sort_sequence int4
  , extra varchar(255)
);