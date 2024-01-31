create view daily_weather as
select
    date_trunc('day', ipwd.dt_iso) dt_iso,
    avg(ipwd.temp) as avg_temp,
    avg(ipwd.temp_min) as avg_temp_min,
    avg(ipwd.temp_max) as avg_temp_max,
    avg(ipwd.wind_deg) as avg_wind_deg,
    avg(ipwd.wind_gust) as avg_wind_gust,
    avg(ipwd.wind_speed) as avg_wind_speed,
    avg(ipwd.snow_1h) as avg_snow_1h,
    avg(ipwd.rain_1h) as avg_rain_1h,
    max(ipwmp.weather_priority) as weather_main_priority,
    max(ipwmp.weather_main) as weather_main
from incident_predictions_weather_data as ipwd
join incident_predictions_weather_main_priority as ipwmp
on ipwd.weather_main = ipwmp.weather_main
where date_trunc('year', ipwd.dt_iso) in
      (
      select distinct date_trunc('year', ipsd.date)
      from incident_predictions_storm_damage ipsd
      )
group by date_trunc('day', ipwd.dt_iso);