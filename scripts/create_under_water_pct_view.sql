create view underwater_pct_view AS
    SELECT
        data.grid_id,
        max(data.sum_area_drainable) AS drainable,
        max(data.sum_area_not_drainable) AS not_drainable,
        max(data.sum_area_drainable) + max(data.sum_area_not_drainable) AS total_underwater
    FROM (
        SELECT
          grid_id,
          drainage,
          SUM(CASE WHEN drainage = 'DRAIN_POSSIBLE' THEN area_covered ELSE 0 END) AS sum_area_drainable,
          SUM(CASE WHEN drainage = 'DRAIN_NOT_POSSIBLE' THEN area_covered ELSE 0 END) AS sum_area_not_drainable
        FROM (
            SELECT
            iph.drainage,
            ipa.grid_id,
            ST_Area(ST_Intersection(iph.geometry, ipa.geometry)) / ST_Area(ipa.geometry) AS area_covered
          FROM
            incident_predictions_highgroundwatermodel iph
            JOIN incident_predictions_amsterdamgridmodel ipa ON ST_Intersects(iph.geometry, ipa.geometry)
        ) AS area_covered
    GROUP BY grid_id, drainage
    ) AS data
    group by data.grid_id;