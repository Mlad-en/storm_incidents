create view tree_age_description as 
select
ipa.grid_id,
count(ipt.tree_age) as tree_count,
avg(ipt.tree_age) mean_tree_age,
coalesce(stddev(ipt.tree_age),0) as std_tree_age,
min(ipt.tree_age) as min_age,
max(ipt.tree_age) as max_age,
percentile_cont(0.25) WITHIN GROUP (ORDER BY tree_age) AS percentile_25,
percentile_cont(0.75) WITHIN GROUP (ORDER BY tree_age) AS percentile_75
from incident_predictions_trees ipt
JOIN incident_predictions_amsterdam_grid ipa
ON ST_Contains(ipa.geometry, ipt.geometry)
group by ipa.grid_id;