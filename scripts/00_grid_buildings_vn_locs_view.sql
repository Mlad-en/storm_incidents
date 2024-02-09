SELECT ipag.grid_id,
       count(*)                                             AS count_building_year,
       round(avg(ipb.construction_year), 0)                 AS avg_building_year,
       count(ipvl.id) + count(vn_locs_no_building_known.id) AS count_vnl_locs
FROM incident_predictions_amsterdam_grid ipag
         JOIN incident_predictions_buildings ipb ON st_intersects(ipag.geometry, ipb.geometry)
         LEFT JOIN incident_predictions_vunerable_locations ipvl ON st_contains(ipb.geometry, ipvl.geometry)
         LEFT JOIN (SELECT ipvl_1.id,
                           ipvl_1.geometry
                    FROM incident_predictions_vunerable_locations ipvl_1
                             LEFT JOIN incident_predictions_buildings ipb_1
                                       ON st_contains(ipb_1.geometry, ipvl_1.geometry)
                    WHERE ipb_1.id IS NULL) vn_locs_no_building_known
                   ON st_contains(ipag.geometry, vn_locs_no_building_known.geometry)
GROUP BY ipag.grid_id