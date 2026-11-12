# SaaS Revenue & Cohort Analytics

**Focus:** SQL · cohort retention · MRR analysis · KPI definitions · executive reporting

A small analytics pipeline built with Python and SQLite. It generates **synthetic subscriptions** and runs SQL-based revenue, monthly active customer, churn, and cohort queries. There is no real customer data.

## Run
```bash
python src/pipeline.py
python -m unittest discover -s tests -v
```

## Data model
`subscriptions(customer_id, start_month, end_month, monthly_fee)` where `end_month` is the first *inactive* month. All fees and dates are fictional.

## Metrics
- **MRR:** sum of recurring fees for subscriptions active in the reporting month (no discounts/taxes).
- **Active accounts:** number of active subscription accounts.
- **Logo churn:** customers lost during a month divided by active customers in the prior month.
- **Cohort retention:** fraction of a signup month's customers still active after N months.

## Business question
Which acquisition cohorts retain best and how much of MRR growth stems from retention versus new acquisition? Production work should add acquisition channels, upgrade/downgrade events, net revenue retention, and explicit timezone and cancellation policies.

See [ROADMAP.md](ROADMAP.md) for future development milestones.
