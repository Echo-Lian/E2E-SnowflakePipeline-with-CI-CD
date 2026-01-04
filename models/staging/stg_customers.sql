{{ config(materialized='ephemeral') }}

select
    customer_id::integer as customer_id,
    customer_name::varchar(100) as customer_name,
    email::varchar(100) as email,
    region::varchar(50) as region,
    signup_date::date as signup_date,
    current_timestamp() as loaded_at
from {{ source('raw_data', 'customers') }}
