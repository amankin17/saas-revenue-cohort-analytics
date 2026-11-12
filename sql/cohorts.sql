-- Retention for each signup cohort at observation month :month.
SELECT start_month AS cohort,
       COUNT(*) AS cohort_size,
       SUM(CASE WHEN end_month IS NULL OR end_month > :month THEN 1 ELSE 0 END) AS still_active
FROM subscriptions
WHERE start_month <= :month
GROUP BY start_month
ORDER BY start_month;
