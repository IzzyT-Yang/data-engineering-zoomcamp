#!/usr/bin/env python
# coding: utf-8

from sqlalchemy import create_engine
import click
import pandas as pd
from tqdm.auto import tqdm

# Handle data dypes
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

@click.command()
@click.option('--year', type=int, default=2021, show_default=True)
@click.option('--month', type=int, default=1, show_default=True)
@click.option('--pg-user', type=str, default='root', show_default=True)
@click.option('--pg-pass', type=str, default='root', show_default=True)
@click.option('--pg-host', type=str, default='localhost', show_default=True)
@click.option('--pg-port', type=int, default=5432, show_default=True)
@click.option('--pg-db', type=str, default='ny_taxi', show_default=True)
@click.option('--chunksize', type=int, default=100000, show_default=True)
@click.option('--target-table', type=str, default='yellow_taxi_data', show_default=True)
def run(year, month, pg_user, pg_pass, pg_host, pg_port, pg_db, chunksize, target_table):

    # Define URL
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}yellow_tripdata_{year:04d}-{month:02d}.csv.gz'


    # Create database connection
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Segment data and ingest into SQL
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize
    )

    first = True
    for df_chunk in tqdm(df_iter):
        if first:
            df_chunk.head(0).to_sql(
                name=target_table, 
                con=engine, 
                if_exists='replace', 
                index=False
            )
            first = False
        df_chunk.to_sql(name=target_table, con=engine, if_exists='append', index=False)

if __name__ == '__main__':
    run()