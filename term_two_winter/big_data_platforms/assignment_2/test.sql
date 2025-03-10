CREATE OR REPLACE TABLE `chicago_taxi_trips.cleaned_chicago_taxi_trips` AS
SELECT *
FROM `bigquery-public-data.chicago_taxi_trips.taxi_trips`
WHERE trip_seconds IS NOT NULL
AND trip_miles IS NOT NULL
AND trip_total IS NOT NULL
AND pickup_latitude IS NOT NULL
AND pickup_longitude IS NOT NULL
AND dropoff_latitude IS NOT NULL
AND dropoff_longitude IS NOT NULL;


SELECT 
    COUNT(*) AS total_rows,

    -- Identifiers
    COUNTIF(unique_key IS NULL) AS missing_unique_key,
    COUNTIF(taxi_id IS NULL) AS missing_taxi_id,

    -- Timestamps
    COUNTIF(trip_start_timestamp IS NULL) AS missing_start_time,
    COUNTIF(trip_end_timestamp IS NULL) AS missing_end_time,

    -- Trip details
    COUNTIF(trip_seconds IS NULL) AS missing_trip_seconds,
    COUNTIF(trip_miles IS NULL) AS missing_trip_miles,

    -- Location data
    COUNTIF(pickup_latitude IS NULL) AS missing_pickup_lat,
    COUNTIF(pickup_longitude IS NULL) AS missing_pickup_long,
    COUNTIF(dropoff_latitude IS NULL) AS missing_dropoff_lat,
    COUNTIF(dropoff_longitude IS NULL) AS missing_dropoff_long,
    COUNTIF(pickup_location IS NULL) AS missing_pickup_location,
    COUNTIF(dropoff_location IS NULL) AS missing_dropoff_location,

    -- Fare & payment
    COUNTIF(fare IS NULL) AS missing_fare,
    COUNTIF(trip_total IS NULL) AS missing_trip_total,
    COUNTIF(tips IS NULL) AS missing_tips,
    COUNTIF(tolls IS NULL) AS missing_tolls,
    COUNTIF(extras IS NULL) AS missing_extras,

    -- Census data
    COUNTIF(pickup_census_tract IS NULL) AS missing_pickup_census,
    COUNTIF(dropoff_census_tract IS NULL) AS missing_dropoff_census,
    COUNTIF(pickup_community_area IS NULL) AS missing_pickup_area,
    COUNTIF(dropoff_community_area IS NULL) AS missing_dropoff_area,

    -- Other business-related info
    COUNTIF(company IS NULL) AS missing_company,
    COUNTIF(payment_type IS NULL) AS missing_payment_type

  FROM `chicago_taxi_trips.cleaned_chicago_taxi_trips`;


UPDATE `chicago_taxi_trips.cleaned_chicago_taxi_trips`
SET tolls = 0
WHERE tolls IS NULL;


UPDATE `chicago_taxi_trips.cleaned_chicago_taxi_trips`
SET company = 'Unknown'
WHERE company IS NULL;


UPDATE `chicago_taxi_trips.cleaned_chicago_taxi_trips`
SET pickup_community_area = 'Unknown'
WHERE pickup_community_area IS NULL;

UPDATE `chicago_taxi_trips.cleaned_chicago_taxi_trips`
SET dropoff_community_area = 'Unknown'
WHERE dropoff_community_area IS NULL;

UPDATE `chicago_taxi_trips.cleaned_chicago_taxi_trips`
SET pickup_census_tract = 'Unknown'
WHERE pickup_census_tract IS NULL;

UPDATE `chicago_taxi_trips.cleaned_chicago_taxi_trips`
SET dropoff_census_tract = 'Unknown'
WHERE dropoff_census_tract IS NULL;





CREATE OR REPLACE TABLE `chicago_taxi_trips.featured_chicago_taxi_trips` AS
SELECT 
    trip_total,  -- Target variable (fare amount)
    
    -- Key numerical features
    trip_seconds / 60 AS trip_duration_mins, 
    trip_miles,
    
    -- Location data
    pickup_latitude, pickup_longitude, 
    dropoff_latitude, dropoff_longitude,
    
    -- Fare breakdowns
    fare, tips, tolls, extras,
    
    -- Categorical features
    payment_type,
    company,
    
    -- Extracted time-based features
    EXTRACT(HOUR FROM trip_start_timestamp) AS trip_hour,
    EXTRACT(DAYOFWEEK FROM trip_start_timestamp) AS trip_day_of_week,
    
    -- Derived trip category based on distance
    CASE 
        WHEN trip_miles < 2 THEN 'Short'
        WHEN trip_miles BETWEEN 2 AND 10 THEN 'Medium'
        ELSE 'Long'
    END AS trip_distance_category,

    -- Census data (keeping as NULL if missing)
    pickup_community_area,
    dropoff_community_area,
    pickup_census_tract,
    dropoff_census_tract

FROM `chicago_taxi_trips.cleaned_chicago_taxi_trips`;


SELECT column_name, data_type 
FROM `chicago_taxi_trips.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'featured_chicago_taxi_trips';


SELECT *
FROM `chicago_taxi_trips.featured_chicago_taxi_trips`
LIMIT 10;


CREATE OR REPLACE MODEL `chicago_taxi_trips.fare_prediction_model`
OPTIONS(
    model_type = 'linear_reg',
    DATA_SPLIT_METHOD = 'AUTO_SPLIT',
    input_label_cols = ['trip_total']
) AS
SELECT 
    -- Target variable
    trip_total,  

    -- Trip details
    trip_duration_mins,
    trip_miles,

    -- Location data
    pickup_latitude, pickup_longitude, 
    dropoff_latitude, dropoff_longitude,

    -- Fare breakdowns
    fare, tips, tolls, extras,

    -- Payment and company details
    payment_type,
    company,

    -- Time-based features
    trip_hour,
    trip_day_of_week,

    -- One-hot encoded trip distance category
    IF(trip_distance_category = 'Short', 1, 0) AS is_short_trip,
    IF(trip_distance_category = 'Medium', 1, 0) AS is_medium_trip,
    IF(trip_distance_category = 'Long', 1, 0) AS is_long_trip

FROM `chicago_taxi_trips.featured_chicago_taxi_trips`;


SELECT *
FROM ML.TRAINING_INFO(MODEL `chicago_taxi_trips.fare_prediction_model`);
