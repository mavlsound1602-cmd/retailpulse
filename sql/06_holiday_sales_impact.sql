-- Sales impact on national holidays vs normal days
WITH holiday_dates AS (
    SELECT DISTINCT date
    FROM raw_holidays
    WHERE locale = 'National'
),
daily_sales AS (
    SELECT 
        t.date,
        ROUND(SUM(t.unit_sales), 0) AS total_units,
        CASE WHEN h.date IS NOT NULL THEN 'Holiday' ELSE 'Normal' END AS day_type
    FROM raw_train t
    LEFT JOIN holiday_dates h ON t.date = h.date
    GROUP BY t.date, h.date
)
SELECT 
    day_type,
    COUNT(*) AS num_days,
    ROUND(AVG(total_units), 0) AS avg_daily_units,
    ROUND(MAX(total_units), 0) AS max_daily_units,
    ROUND(MIN(total_units), 0) AS min_daily_units
FROM daily_sales
GROUP BY day_type;
