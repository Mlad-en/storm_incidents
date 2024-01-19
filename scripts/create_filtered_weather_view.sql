create view filtered_weather as
SELECT
    dt_iso, temp, dew_point, feels_like, temp_min, temp_max, pressure,
    humidity, wind_speed, wind_deg, wind_gust, rain_1h, rain_3h, snow_1h, weather_main
FROM (
SELECT ipwd.id, ipwd.dt_iso, ipwd.temp, ipwd.dew_point, ipwd.feels_like, ipwd.temp_min, ipwd.temp_max,
ipwd.pressure, ipwd.humidity, ipwd.wind_speed, ipwd.wind_deg, ipwd.wind_gust, ipwd.rain_1h,
ipwd.rain_3h, ipwd.snow_1h, ipwd.weather_main,
row_number() OVER (PARTITION BY ipwd.dt_iso ORDER BY ipwmp.weather_priority DESC) AS rnk
FROM incident_predictions_weather_data ipwd
JOIN incident_predictions_weather_main_priority ipwmp ON ipwd.weather_main::text = ipwmp.weather_main::text
WHERE (EXTRACT(Year FROM ipwd.dt_iso) IN (SELECT DISTINCT EXTRACT(Year FROM ipsd.date) AS "extract"
FROM incident_predictions_storm_damage ipsd))
AND EXTRACT(Year FROM ipwd.dt_iso) <> 2005::numeric) filterted_data
WHERE rnk = 1
and not (wind_gust <= 5 and wind_speed <= 5 and weather_main not in ('Rain', 'Thunderstorm', 'Snow', 'Squall'));