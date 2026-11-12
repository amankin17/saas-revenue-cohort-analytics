-- :month example '2026-06', end_month exclusive
SELECT :month AS month,
       COUNT(*) AS active_accounts,
       ROUND(COALESCE(SUM(monthly_fee),0),2) AS mrr
FROM subscriptions
WHERE start_month <= :month AND (end_month IS NULL OR end_month > :month);
