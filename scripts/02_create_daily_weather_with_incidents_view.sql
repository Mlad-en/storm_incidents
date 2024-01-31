create view daily_weather_with_incidents as
select distinct
dw.dt_iso,
dw.avg_temp,
dw.avg_temp_min,
dw.avg_temp_max,
dw.avg_wind_deg,
dw.avg_wind_gust,
dw.avg_wind_speed,
dw.avg_snow_1h,
dw.avg_rain_1h,
dw.weather_main_priority,
dw.weather_main,
sum(coalesce(ctipgd.count_incidents, 0)) over (partition by dw.dt_iso) as count_incidents,
sum(coalesce(ctipgd.count_incidents, 0)) over (partition by dw.dt_iso) > 0 as has_incident
from daily_weather dw
left join count_tree_incidents_per_grid_date ctipgd
on dw.dt_iso = ctipgd.date;