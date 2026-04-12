# dbt

## Steps
- Set up dbt cloud
  - Create a bigquery connection through a servie account
  - Create a new project in dbt cloud, configure dataset, location (us-east4), and connection (bigquery)
  - Connect to a specific subdir in github repo
  - `dbt init` to generate project structure
- Sources
  - sources.yml in models/staging
- Models
  - green_tripdata.sql in models/staging (use formats like `{{ source('raw_data', 'green_tripdata') }}`)