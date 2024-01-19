create view count_tree_incidents_per_grid_date as
select
ipag.grid_id,
ipsd.date,
extract(HOUR from ipsd.incident_start_time) as hour,
sum(ipsd.incident_duration) as total_incident_duration,
max(ipsd.incident_priority) as max_incident_priority,
count(*) as count_incidents
from incident_predictions_storm_damage as ipsd
join public.incident_predictions_amsterdam_grid as ipag
on st_contains(ipag.geometry, ipsd.geometry)
where damage_type = 'Tree'
group by ipag.grid_id, ipsd.date, extract(HOUR from ipsd.incident_start_time);