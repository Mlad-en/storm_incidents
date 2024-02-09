create view sample_randomly_daily_data as
    WITH date_hours AS (
    SELECT DISTINCT DATE_TRUNC('day', ipwd.dt_iso) AS date_part
    FROM incident_predictions_weather_data ipwd
),
sample_hours AS (
    SELECT date_part, array_agg(EXTRACT(HOUR FROM ipwd.dt_iso)) AS hours
    FROM incident_predictions_weather_data ipwd
    CROSS JOIN date_hours
    WHERE DATE_TRUNC('day', ipwd.dt_iso) = date_part
    GROUP BY date_part
)

select DATE_TRUNC('day', ipwd.dt_iso) as date_time,
        avg(ipwd.temp)                       AS avg_temp,
       avg(ipwd.temp_min)                   AS avg_temp_min,
       avg(ipwd.temp_max)                   AS avg_temp_max,
       avg(ipwd.wind_deg)                   AS avg_wind_deg,
       avg(ipwd.wind_gust)                  AS avg_wind_gust,
       avg(ipwd.wind_speed)                 AS avg_wind_speed,
       avg(ipwd.snow_1h)                    AS avg_snow_1h,
       avg(ipwd.rain_1h)                    AS avg_rain_1h,
       max(ipwmp.weather_priority)          AS weather_main_priority,
       max(ipwmp.weather_main::text)        AS weather_main
from (
    SELECT date_part, (hours[1 + (random() * array_length(hours, 1))])::int AS sampled_hour
FROM sample_hours
CROSS JOIN generate_series(1, 6) AS s
where date_trunc('day', date_part) not in (select ipsd.date from incident_predictions_storm_damage ipsd)
     ) as sampled_date_hours
join incident_predictions_weather_data ipwd
    on DATE_TRUNC('day', ipwd.dt_iso) = date_trunc('day', date_part)
    and extract(hour from ipwd.dt_iso) = sampled_hour
join public.incident_predictions_weather_main_priority ipwmp on ipwd.weather_main = ipwmp.weather_main
where DATE_TRUNC('year', ipwd.dt_iso) in (select distinct date_trunc('year', ipsd.date) AS date_trunc
        FROM incident_predictions_storm_damage ipsd)
group by DATE_TRUNC('day', ipwd.dt_iso);