---
type: Table
title: Customer Orders
description: Primary transaction table recording every completed order across web, mobile, and API channels.
resource: https://console.cloud.google.com/bigquery?p=enterprise-corp&d=analytics&t=orders
tags: [data, orders, e-commerce, core]
status: stable
generated:
  by: metadata-agent/gpt-4o
  at: 2026-08-31T09:00:00Z
verified:
  - by: human:data-engineer
    at: 2026-08-31T09:30:00Z
sources:
  - id: enterprise-data-dictionary
    resource: https://internal.company.com/data/dictionary/orders
    title: Enterprise Data Governance Dictionary
    author: Data Engineering Group
---

# Schema

| Column Name | Data Type | Nullable | Description |
| :--- | :--- | :--- | :--- |
| `order_id` | STRING | NO | Globally unique primary key (UUIDv4). |
| `customer_id` | STRING | NO | Foreign key referencing [Customers](/tables/customers.md). |
| `gross_amount_usd` | NUMERIC | NO | Total transaction amount before discounts and taxes. |
| `net_amount_usd` | NUMERIC | NO | Settled revenue amount in USD. |
| `order_status` | STRING | NO | Enum: `PENDING`, `COMPLETED`, `REFUNDED`, `CANCELLED`. |
| `created_at` | TIMESTAMP | NO | Order placement timestamp in UTC. |

# Joins & Relationships

* **Customer Details**: Join on `customer_id` with [Customers](/tables/customers.md).
* **Payment Records**: Join on `order_id` with [Payment Events](/tables/payment-events.md).

# Example Query

```sql
SELECT
  DATE_TRUNC(created_at, DAY) AS order_date,
  COUNT(DISTINCT order_id) AS total_orders,
  SUM(net_amount_usd) AS daily_revenue_usd
FROM `enterprise-corp.analytics.orders`
WHERE order_status = 'COMPLETED'
  AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1
ORDER BY 1 DESC;
```

[^enterprise-data-dictionary]: Enterprise Data Governance Dictionary
