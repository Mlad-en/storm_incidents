create view sample_weather_with_incidents as
select
    date_trunc('day', ioe.dt_iso),
       avg(ioe.temp)                       AS avg_temp,
       avg(ioe.temp_min)                   AS avg_temp_min,
       avg(ioe.temp_max)                   AS avg_temp_max,
       avg(ioe.wind_deg)                   AS avg_wind_deg,
       avg(ioe.wind_gust)                  AS avg_wind_gust,
       avg(ioe.wind_speed)                 AS avg_wind_speed,
       avg(ioe.snow_1h)                    AS avg_snow_1h,
       avg(ioe.rain_1h)                    AS avg_rain_1h,
       max(ipwmp.weather_priority)         AS weather_main_priority,
       max(ipwmp.weather_main)             AS weather_main
from (
    select *,
  CASE
   WHEN lag(incident_occured, 0) OVER (ORDER BY dt_iso DESC) IS TRUE THEN TRUE
   WHEN lag(incident_occured, 1) OVER (ORDER BY dt_iso DESC) IS TRUE THEN TRUE
   WHEN lag(incident_occured, 2) OVER (ORDER BY dt_iso DESC) IS TRUE THEN TRUE
   WHEN lag(incident_occured, 3) OVER (ORDER BY dt_iso DESC) IS TRUE THEN TRUE
   WHEN lag(incident_occured, 4) OVER (ORDER BY dt_iso DESC) IS TRUE THEN TRUE
   WHEN lag(incident_occured, 5) OVER (ORDER BY dt_iso DESC) IS TRUE THEN TRUE
   ELSE FALSE
END AS incident_occured_extended
    from (
        select ipwd.*, ipsd.id as incident_id, ipsd.incident_start_time,
       coalesce(
               extract(hour from ipwd.dt_iso) = extract(hour from ipsd.incident_start_time),
               false
       ) as incident_occured
from incident_predictions_weather_data ipwd
left join incident_predictions_storm_damage ipsd
on date_trunc('day', ipwd.dt_iso) = ipsd.date
and ipsd.damage_type = 'Tree'
         ) as ii
order by dt_iso
     ) as ioe
join incident_predictions_weather_main_priority ipwmp
on ipwmp.weather_main = ioe.weather_main
where ioe.incident_occured_extended is true and incident_id is not null
group by date_trunc('day', ioe.dt_iso);