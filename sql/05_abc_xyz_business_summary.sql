-- Business impact summary by ABC-XYZ segment
SELECT
    ABC_XYZ,
    COUNT(*) AS item_count,
    ROUND(AVG(mean_sales), 2) AS avg_daily_demand,
    ROUND(SUM(annual_revenue), 0) AS total_annual_revenue,
    ROUND(SUM(annual_revenue_at_risk), 0) AS total_revenue_at_risk,
    ROUND(SUM(annual_stockout_cost), 0) AS total_stockout_cost,
    COUNT(CASE WHEN alert_urgency = 'Critical' THEN 1 END) AS critical_alerts,
    COUNT(CASE WHEN alert_urgency = 'Reorder Now' THEN 1 END) AS reorder_alerts
FROM business_outputs
GROUP BY ABC_XYZ
ORDER BY total_annual_revenue DESC;
