CREATE TABLE fw.category (
    case_code varchar(1)
  , category_code varchar(3)
  , category_text varchar(100)
  , display_level int4
  , selectable varchar(1)
  , sort_sequence int4
  , extra varchar(255)
  , PRIMARY KEY (case_code, category_code))
;