---
type: Attested Computation
title: Customer Acquisition Cost (CAC)
description: Sanctioned analytical computation for computing blended customer acquisition cost over a defined fiscal window.
tags: [metrics, finance, computation, verified]
status: stable
runtime: sql
parameters:
  - name: start_date
    type: DATE
    required: true
  - name: end_date
    type: DATE
    required: true
executor:
  resource: /references/executors/run_query.py
attester:
  resource: /references/attesters/cac_attester.py
generated:
  by: finance-agent/gemini-2.5-pro
  at: 2026-08-31T10:00:00Z
verified:
  - by: human:cfo
    at: 2026-08-31T11:00:00Z
sources:
  - id: finance-policy-2026
    resource: /policies/revenue-recognition.md
    title: 2026 Corporate Financial Policy on Sales and Marketing Amortization
    author: team:finance
---

# Definition

Customer Acquisition Cost (CAC) measures total sales and marketing expenditure divided by the total number of newly acquired paying accounts during a given period.[^finance-policy-2026]

# Computation

```sql
WITH sales_marketing_costs AS (
  SELECT
    DATE_TRUNC(expense_date, MONTH) AS cost_month,
    SUM(amount_usd) AS total_expense_usd
  FROM `analytics.financials.general_ledger`
  WHERE category IN ('Sales Payroll', 'Paid Media', 'Marketing Software')
    AND expense_date BETWEEN @start_date AND @end_date
  GROUP BY 1
),
new_customers AS (
  SELECT
    DATE_TRUNC(created_at, MONTH) AS signup_month,
    COUNT(DISTINCT account_id) AS new_accounts
  FROM `analytics.production.accounts`
  WHERE is_paying = TRUE
    AND first_conversion_date BETWEEN @start_date AND @end_date
  GROUP BY 1
)
SELECT
  s.cost_month,
  s.total_expense_usd,
  c.new_accounts,
  SAFE_DIVIDE(s.total_expense_usd, c.new_accounts) AS blended_cac_usd
FROM sales_marketing_costs s
JOIN new_customers c ON s.cost_month = c.signup_month
ORDER BY s.cost_month ASC;
```

# Attestation & Verification

The attester script verifies that:
1. No unapproved expense categories are included in the numerator.
2. Only verified first-time paying customer IDs are counted in the denominator.

[^finance-policy-2026]: 2026 Corporate Financial Policy on Sales and Marketing Amortization
