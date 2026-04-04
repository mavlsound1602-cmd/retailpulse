-- Top product families by total units sold
SELECT 
    i.family,
    ROUND(SUM(t.unit_sales), 0) AS total_units,
    COUNT(DISTINCT t.store_nbr) AS stores_selling,
    COUNT(DISTINCT t.item_nbr) AS unique_items
FROM raw_train t
JOIN raw_items i ON t.item_nbr = i.item_nbr
GROUP BY i.family
ORDER BY total_units DESC
LIMIT 10;
