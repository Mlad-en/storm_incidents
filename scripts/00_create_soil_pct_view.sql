create view soil_pct_view AS
select
grid_id,
max(sum_area_1) as sum_area_1,
max(sum_area_2) as sum_area_2,
max(sum_area_3) as sum_area_3,
max(sum_area_4) as sum_area_4,
max(sum_area_5) as sum_area_5,
max(sum_area_6) as sum_area_6,
max(sum_area_7) as sum_area_7,
max(sum_area_20) as sum_area_20,
max(sum_area_remediation) as sum_area_remediation,
max(sum_area_unknown) as sum_area_unknown
from (
SELECT
grid_id,
zone,
SUM(CASE WHEN zone = '1' THEN area_covered ELSE 0 END) AS sum_area_1,
SUM(CASE WHEN zone = '2' THEN area_covered ELSE 0 END) AS sum_area_2,
SUM(CASE WHEN zone = '3' THEN area_covered ELSE 0 END) AS sum_area_3,
SUM(CASE WHEN zone = '4' THEN area_covered ELSE 0 END) AS sum_area_4,
SUM(CASE WHEN zone = '5' THEN area_covered ELSE 0 END) AS sum_area_5,
SUM(CASE WHEN zone = '6' THEN area_covered ELSE 0 END) AS sum_area_6,
SUM(CASE WHEN zone = '7' THEN area_covered ELSE 0 END) AS sum_area_7,
SUM(CASE WHEN zone = '20' THEN area_covered ELSE 0 END) AS sum_area_20,
SUM(CASE WHEN zone = 'w' THEN area_covered ELSE 0 END) AS sum_area_unknown,
SUM(CASE WHEN zone = 's' THEN area_covered ELSE 0 END) AS sum_area_remediation
FROM
(SELECT
ips.zone,
ipa.grid_id,
ST_Area(ST_Intersection(ips.geometry, ipa.geometry)) / ST_Area(ipa.geometry) AS area_covered
FROM
incident_predictions_soil ips
JOIN incident_predictions_amsterdam_grid ipa ON ST_Intersects(ips.geometry, ipa.geometry)
)  AS area_covered
GROUP BY grid_id, zone
) as ac
GROUP BY grid_id;
