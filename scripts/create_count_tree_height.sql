create view count_tree_height as
select grid_id,
COUNT(CASE WHEN tree_height = 'HEIGHT_UP_TO_6M' THEN 1 ELSE 0 END) AS count_up_to_6,
COUNT(CASE WHEN tree_height = 'HEIGHT_6_TO_9M' THEN 1 ELSE 0 END) AS count_6_to_9,
COUNT(CASE WHEN tree_height = 'HEIGHT_9_TO_12M' THEN 1 ELSE 0 END) AS count_9_to_12,
COUNT(CASE WHEN tree_height = 'HEIGHT_12_TO_15M' THEN 1 ELSE 0 END) AS count_12_to_15,
COUNT(CASE WHEN tree_height = 'HEIGHT_15_TO_18M' THEN 1 ELSE 0 END) AS count_15_to_18,
COUNT(CASE WHEN tree_height = 'HEIGHT_18_TO_24M' THEN 1 ELSE 0 END) AS count_18_to_24,
COUNT(CASE WHEN tree_height = 'HEIGHT_OVER_24M' THEN 1 ELSE 0 END) AS count_over_24,
COUNT(CASE WHEN tree_height = 'HEIGHT_UNKNOWN' THEN 1 ELSE 0 END) AS count_unknown
from incident_predictions_treesmodel ipt
JOIN incident_predictions_amsterdamgridmodel ipa
ON ST_Contains(ipa.geometry, ipt.geometry)
group by ipa.grid_id;