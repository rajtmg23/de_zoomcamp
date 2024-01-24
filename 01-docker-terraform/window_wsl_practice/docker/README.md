## Creating volume for windows wsl:
```bash
docker volume Create --name dtc_postgres_volume_local -d local
```
## Running Postgres server with the necessary env info:
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v dtc_postgres_volume_local:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

### If we want to interact with the database from the command line. Then it can be done through `pgcli`. Install the `pgcli` module first.
```bash
pip install pgcli
```
**The command for connecting to the db is:**
```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

Now we have a postgres server running. To connect pgadmin with the postgres server they need to be on same network.
To create network we use the following command.
```bash
docker network create pg-network  
#pg-network is the network name.
```
#### Running the `postgres:13` & `dpage/pgadmin14` image on the pre-defined `pg-network`.
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v dtc_postgres_volume_local:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13


docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pg-admin4 \
  dpage/pgadmin4
```
**If all thing goes well then now we can build the `docker-compose.yaml` file for running the both image with a single command `docker-compose up`. The sample of the docker file can be as follows:**
```docker

services:
  pg-database:
    image: postgres:13
    environment:
      - POSTGRES_USER=root
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
    volumes:
      - dtc_postgres_volume_local:/var/lib/postgresql/data:rw
    ports:
      - 5432:5432

  pg-admin4:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - 8080:80


```
_For windows-wsl this extra code is added. We don't need this code for linux._
```docker
volumes:
  dtc_postgres_volume_local:
    external: true
```
After creation of `docker-compose.yaml` file. We can simple type the following command to run both the container:
```bash
docker-compose up
```
After finishing the work. Simply we can type the following command for terminating the container:
```bash
docker-compose down
# docker-compose up -d (runs containers in detach mode)
```

For inserting datas to the database table we can using the following python script.
```python
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
    csv_name = "output.csv"

    # download the csv
    os.system(f"wget {url} -O {csv_name}")


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
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"{table_name} table successfully created.")
    
    print(f"Writing datas to table.... {table_name}.")
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)


    while True:
        try:
            t_start = time()

            df = next(df_iter)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)

            df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

            t_end = time()

            print("Inserted another chunk, took %.3f second" % (t_end - t_start))
            
        except StopIteration:
            print('completed')
            break


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
```
Run the following command from the terminal.
```bash
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url="http://172.18.88.69:8000/ubuntu_virtualbox/yellow_tripdata_2021-01.csv"
```
**If all things goes the desired way then we can build a docker image with the following docker file. The code for docker file is given below:**
```docker
FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app

COPY ingest_data.py ingest_data.py

ENTRYPOINT [ "python", "ingest_data.py" ]
```
Now run the following command from terminal to build a image:
```bash
docker build -t tai_ingest:v001 .
```
The dataset used on the example is given below:
[link](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz)

For running a local http server. We can use this command.
```bash
python -m http.server
```
_Now we can open our local server from `http://localhost:8080`_

After successful creation of our `taxi_ingest:v001` image it can be run as a docker container with the following credentials.
```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```
_where `--network=pg-network` is the network used by our previous containers running previously._
To view the list of network available in docker. We can use the following command.
```bash
docker network ls
```


