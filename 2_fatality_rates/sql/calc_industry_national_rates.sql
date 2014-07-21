UPDATE industries 
SET fatals_per_100k = (fatals_total / emplvl_total) * 100000;
