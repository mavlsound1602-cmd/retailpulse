-- Sales performance by store type
SELECT 
    s.type AS store_type,
    COUNT(*) AS total_transactions,
    ROUND(SUM(t.unit_sales), 0) AS total_units_sold,
    ROUND(AVG(t.unit_sales), 2) AS avg_units_per_transaction
FROM raw_train t
JOIN raw_stores s ON t.store_nbr = s.store_nbr
GROUP BY s.type
ORDER BY total_units_sold DESC;
