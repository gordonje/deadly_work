-- residential specialty trades in TX
select 
	  year
	, sum(fatals) as fatals
	, sum(emplvl) as emplvl
	, ROUND(sum(fatals) / sum(emplvl) * 100000, 2) as fatals_per_100k 
from states_industries_years
where state_code = '48'
and industry_code in ('238111','238121','238131','238141','238161','238171','238191','238211','238221','238291','238311','238321','238331','238341','238351','238391','238911','238991')
group by year
order by year;

-- non-residential specialty trades in TX
select 
	  year
	, sum(fatals) as fatals
	, sum(emplvl) as emplvl
	, ROUND(sum(fatals) / sum(emplvl) * 100000, 2) as fatals_per_100k 
from states_industries_years
where state_code = '48'
and industry_code in ('238112','238122','238132','238142','238152','238162','238172','238192','238212','238222','238292','238312','238322','238352','238392','238912','238992')
group by year
order by year;