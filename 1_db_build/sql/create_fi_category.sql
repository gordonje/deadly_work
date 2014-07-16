CREATE TABLE fi.category (
    case_code varchar(1)
  , category_code varchar(3)
  , category_text varchar(100)
  , extra varchar(255)
  , PRIMARY KEY (case_code, category_code))
;