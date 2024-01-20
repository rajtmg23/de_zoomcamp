#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os



def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = "yellow_tripdata_2021-01.csv"

    # download the csv
    # os.system(f"wget {url} -O {csv_name}")


    # Creating connection to the POSTGRESQL
    print("Connecting to db......")
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    try:
        with engine.connect() as connection_str:
            print(f'Successfully connected to the {db} database')
    except Exception as ex:
        print(f'Sorry failed to connect: {ex}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    df = next(df_iter)

    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

    print(f"Creating table {table_name}.")
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    print(f"{table_name} table successfully created.")
    
    print(f"Writing datas to table.... {table_name}.")
    df.to_sql(name=table_name, con=engine, if_exists='append')


    while True:
        t_start = time()

        df = next(df_iter)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')

        t_end = time()

        print("Inserted another chunk, took %.3f second" % (t_end - t_start))


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Ingest CSV to Postgres')

    parser.add_argument('--user', help='user name for postgres server')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='db name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)


