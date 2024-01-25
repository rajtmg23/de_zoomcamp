#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from time import time
import os

df = pd.read_csv("/home/raju/de_zoomcamp/de_zoomcamp/datasets/taxi_zone_lookup.csv")

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Testing connection
try:
    with engine.connect() as connection_str:
        print('Successfully connected to the PostgreSQL database')
except Exception as ex:
    print(f'Sorry failed to connect: {ex}')

print("Writing datas to the db.....")
# Creating table 
df.head(0).to_sql(name='taxi_zones', con=engine, if_exists='replace', index=False)

# Inserting data in the table.
df.to_sql(name='taxi_zones', con=engine, if_exists='append', index=False)
print("Data written successfully.")
