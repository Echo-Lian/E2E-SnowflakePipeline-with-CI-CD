{{ config(materialized='view') }}

with customer_metrics as (
    select
        region,
        count(customer_id) as total_customers,
        avg(datediff('day', signup_date, current_date())) as avg_days_since_signup
    from {{ ref('stg_customers') }}
    group by region
)

select
    region,
    total_customers,
    avg_days_since_signup,
    case
        when total_customers > 30 then 'High'
        when total_customers > 15 then 'Medium'
        else 'Low'
    end as customer_density_category
from customer_metrics
order by total_customers desc
