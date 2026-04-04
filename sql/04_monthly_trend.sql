-- Monthly sales trend with active store count
SELECT 
    YEAR(CAST(date AS DATE)) AS year,
    MONTH(CAST(date AS DATE)) AS month,
    ROUND(SUM(unit_sales), 0) AS total_units,
    COUNT(DISTINCT store_nbr) AS active_stores
FROM raw_train
GROUP BY year, month
ORDER BY year, month;
