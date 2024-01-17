create view count_tree_diameter as
select grid_id,
COUNT(CASE WHEN trunk_diameter_class = 'FROM_0_1_TO_0_2_M' THEN 1 ELSE 0 END) AS count_01_02,
COUNT(CASE WHEN trunk_diameter_class = 'FROM_0_2_TO_0_3_M' THEN 1 ELSE 0 END) AS count_02_03,
COUNT(CASE WHEN trunk_diameter_class = 'FROM_0_3_TO_0_5_M' THEN 1 ELSE 0 END) AS count_03_05,
COUNT(CASE WHEN trunk_diameter_class = 'FROM_0_5_TO_1_M' THEN 1 ELSE 0 END) AS count_05_1,
COUNT(CASE WHEN trunk_diameter_class = 'FROM_1_TO_1_5_M' THEN 1 ELSE 0 END) AS count_1_15,
COUNT(CASE WHEN trunk_diameter_class = 'OVER_1_5_M' THEN 1 ELSE 0 END) AS count_over_15,
COUNT(CASE WHEN trunk_diameter_class = 'UNKNOWN' THEN 1 ELSE 0 END) AS count_unknown
from incident_predictions_trees ipt
JOIN incident_predictions_amsterdam_grid ipa
ON ST_Contains(ipa.geometry, ipt.geometry)
group by ipa.grid_id;