create view building_pct_view AS
select grid_id, SUM(area_covered) AS sum_area_building
from (select
    ipag.grid_id,
    ST_Area(ST_Intersection(ipag.geometry, ipb.geometry)) / ST_Area(ipag.geometry)::float AS area_covered
from incident_predictions_amsterdam_grid ipag
left join public.incident_predictions_buildings ipb
on st_intersects(ipag.geometry, ipb.geometry)
where st_isvalid(ipb.geometry) is TRUE
) as a
group by grid_id