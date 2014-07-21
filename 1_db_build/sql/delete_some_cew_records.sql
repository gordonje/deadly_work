DELETE 
FROM cew.annual_averages_2012 
WHERE (agglvl_code >= 30 AND agglvl_code <= 49)
OR agglvl_code >= 70;