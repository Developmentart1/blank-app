INSERT INTO dim_time (date, year, quarter, month, week, day)
SELECT d::date AS date,
       EXTRACT(YEAR FROM d)::INT AS year,
       EXTRACT(QUARTER FROM d)::INT AS quarter,
       EXTRACT(MONTH FROM d)::INT AS month,
       EXTRACT(WEEK FROM d)::INT AS week,
       EXTRACT(DAY FROM d)::INT AS day
FROM generate_series('2020-01-01'::date, '2030-12-31'::date, '1 day'::interval) d
ON CONFLICT (date) DO NOTHING;
