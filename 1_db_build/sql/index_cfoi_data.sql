CREATE INDEX alldata_series_ind ON fw.alldata (series_id);

CREATE INDEX alldata_year_ind ON fw.alldata (year);

CREATE INDEX alldata_value_ind ON fw.alldata (value);

CREATE INDEX alldata_series_year_ind ON fw.alldata (series_id, year);


CREATE INDEX current_series_ind ON fw.current (series_id);

CREATE INDEX current_year_ind ON fw.current (year);

CREATE INDEX current_value_ind ON fw.current (value);

CREATE INDEX current_series_year_ind ON fw.current (series_id, year);


CREATE INDEX alldata_series_ind ON fi.alldata (series_id);

CREATE INDEX alldata_year_ind ON fi.alldata (year);

CREATE INDEX alldata_value_ind ON fi.alldata (value);

CREATE INDEX alldata_series_year_ind ON fi.alldata (series_id, year);


CREATE INDEX current_series_ind ON fi.current (series_id);

CREATE INDEX current_year_ind ON fi.current (year);

CREATE INDEX current_value_ind ON fi.current (value);

CREATE INDEX current_series_year_ind ON fi.current (series_id, year);