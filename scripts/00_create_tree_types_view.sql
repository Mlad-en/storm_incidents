create view count_tree_types as
select grid_id,
sum(CASE WHEN tree_type_eng = 'Tree not growing freely' THEN 1 ELSE 0 END) AS count_type_not_free_growing,
sum(CASE WHEN tree_type_eng = 'Tree growing freely' THEN 1 ELSE 0 END) AS count_type_free_growing,
sum(CASE WHEN tree_type_eng = 'Fruit tree' THEN 1 ELSE 0 END) AS count_type_fruit,
sum(CASE WHEN tree_type_eng = 'Candelabra tree' THEN 1 ELSE 0 END) AS count_type_candelabra,
sum(CASE WHEN tree_type_eng = 'Pollard tree' THEN 1 ELSE 0 END) AS count_type_pollard,
sum(CASE WHEN tree_type_eng = 'Espalier' THEN 1 ELSE 0 END) AS count_type_espalier,
sum(CASE WHEN tree_type_eng = 'Stump' THEN 1 ELSE 0 END) AS count_type_stump,
sum(CASE WHEN tree_type_eng = 'Topiary tree' THEN 1 ELSE 0 END) AS count_type_topiary,
sum(CASE WHEN tree_type_eng = 'MISSING/UNKNOWN' THEN 1 ELSE 0 END) AS count_type_missing
from (
    select coalesce(iptrans.english_name, 'MISSING/UNKNOWN') tree_type_eng, ipag.grid_id
    from incident_predictions_trees ipt
    left join incident_predictions_tree_type_translations iptrans
    on ipt.tree_type = iptrans.dutch_name
    join incident_predictions_amsterdam_grid ipag
    on st_contains(ipag.geometry, ipt.geometry)
     ) as tree_types
group by grid_id
;
