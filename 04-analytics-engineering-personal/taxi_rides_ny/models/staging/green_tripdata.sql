select filename from {{ source('raw_data', 'green_tripdata') }}
limit 100
