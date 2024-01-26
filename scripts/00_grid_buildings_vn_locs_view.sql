create view grid_buildings_vn_locs as
select
distinct ipag.grid_id,
count(ipb.construction_year) over (partition by ipag.grid_id),
round(avg(ipb.construction_year) over (partition by ipag.grid_id), 0) as avg_year,
count_vnl_locs
from incident_predictions_amsterdam_grid ipag
join incident_predictions_buildings ipb
on ST_Intersects(ipag.geometry, ipb.geometry)
join (select coalesce(ipb.geometry, ipvl.geometry) as geometry, count(ipvl."type") count_vnl_locs
from incident_predictions_vunerable_locations ipvl
left join incident_predictions_buildings ipb
on st_contains(ipb.geometry, ipvl.geometry)
group by coalesce(ipb.geometry, ipvl.geometry)) as count_vunerable
on st_intersects(ipag.geometry, count_vunerable.geometry);
