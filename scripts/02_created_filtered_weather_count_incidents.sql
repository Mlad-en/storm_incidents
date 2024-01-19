create view filtered_weather_with_count_incidents as
select dt_iso, temp, dew_point, feels_like, temp_min, temp_max, pressure,
    humidity, wind_speed, wind_deg, wind_gust, rain_1h, rain_3h, snow_1h, weather_main,
    coalesce(grid_id, 'not_data') as grid_id,
    coalesce(max_incident_priority, 0) as max_incident_priority,
    coalesce(count_incidents, 0) as count_incidents,
    case when count_incidents is not null then 1 else 0 end as has_incident
from filtered_weather fw
left join count_tree_incidents_per_grid_date ctipgd
on extract(hour from fw.dt_iso) = ctipgd."hour"
and date_trunc('day', fw.dt_iso) = ctipgd."date" ;