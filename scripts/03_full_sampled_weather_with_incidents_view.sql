create view full_sampled_weather_with_incidents as
    select DISTINCT sw.date_time as dt_iso,
                sw.avg_temp,
                sw.avg_temp_min,
                sw.avg_temp_max,
                sw.avg_wind_deg,
                sw.avg_wind_gust,
                sw.avg_wind_speed,
                sw.avg_snow_1h,
                sw.avg_rain_1h,
                sw.weather_main_priority,
                sw.weather_main,
                sum(COALESCE(ctipgd.count_incidents, 0)) OVER (PARTITION BY sw.date_time) AS count_incidents,
                sum(COALESCE(ctipgd.count_incidents, 0)) OVER (PARTITION BY sw.date_time) > 0 as has_incident
from (
    select *
from sample_randomly_daily_data
union
select *
from sample_weather_with_incidents
     ) sw
LEFT JOIN count_tree_incidents_per_grid_date ctipgd ON sw.date_time = ctipgd.date;