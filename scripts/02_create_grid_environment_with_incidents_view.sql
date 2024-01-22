create view grid_environment_with_incidents as
select em.*, coalesce(has_incidents.has_incident, 0) as has_incident
from environment_metrics em
left join (
select distinct ipag.grid_id, 1 as has_incident
from incident_predictions_storm_damage ipsd
join incident_predictions_amsterdam_grid ipag
on st_contains(ipag.geometry, ipsd.geometry)
where ipsd.damage_type = 'Tree'
) as has_incidents
on em.grid_id = has_incidents.grid_id;