create view count_species as
select grid_id,
sum(CASE WHEN species_name_short = 'Acer' THEN 1 ELSE 0 END) AS count_acer,
sum(CASE WHEN species_name_short = 'Alnus' THEN 1 ELSE 0 END) AS count_alnus,
sum(CASE WHEN species_name_short = 'Betula' THEN 1 ELSE 0 END) AS count_betula,
sum(CASE WHEN species_name_short = 'Carpinus' THEN 1 ELSE 0 END) AS count_carpinus,
sum(CASE WHEN species_name_short = 'Crataegus' THEN 1 ELSE 0 END) AS count_crataegus,
sum(CASE WHEN species_name_short = 'Fraxinus' THEN 1 ELSE 0 END) AS count_fraxinus,
sum(CASE WHEN species_name_short = 'Malus' THEN 1 ELSE 0 END) AS count_malus,
sum(CASE WHEN species_name_short = 'Onbekend' THEN 1 ELSE 0 END) AS count_onbekend,
sum(CASE WHEN species_name_short = 'Overig' THEN 1 ELSE 0 END) AS count_overig,
sum(CASE WHEN species_name_short = 'Platanus' THEN 1 ELSE 0 END) AS count_platanus,
sum(CASE WHEN species_name_short = 'Populus' THEN 1 ELSE 0 END) AS count_populus,
sum(CASE WHEN species_name_short = 'Prunus' THEN 1 ELSE 0 END) AS count_prunus,
sum(CASE WHEN species_name_short = 'Quercus' THEN 1 ELSE 0 END) AS count_quercus,
sum(CASE WHEN species_name_short = 'Robinia' THEN 1 ELSE 0 END) AS count_robinia,
sum(CASE WHEN species_name_short = 'Salix' THEN 1 ELSE 0 END) AS count_salix,
sum(CASE WHEN species_name_short = 'Tilia' THEN 1 ELSE 0 END) AS count_tilia,
sum(CASE WHEN species_name_short = 'Ulmus' THEN 1 ELSE 0 END) AS count_ulmus
from incident_predictions_trees ipt
join incident_predictions_amsterdam_grid ipag
on st_contains(ipag.geometry, ipt.geometry)
group by ipag.grid_id;
