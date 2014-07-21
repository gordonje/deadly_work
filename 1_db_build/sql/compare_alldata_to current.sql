-- count is zero
SELECT COUNT(*)
FROM fw.alldata a
JOIN fw.current b
ON a.series_id = b.series_id
AND a.year = b.year
WHERE a.value <> b.value;

-- count is zero
SELECT COUNT(*)
FROM fi.alldata a
JOIN fi.current b
ON a.series_id = b.series_id
AND a.year = b.year
WHERE a.value <> b.value;