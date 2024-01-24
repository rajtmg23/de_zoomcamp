
**Creating a image from the docker file.**
Sample code for the docker file.
```docker
FROM python:3.9.1

RUN pip install pandas

WORKDIR /app
COPY . .

ENTRYPOINT [ "bash" ]
```
Run the following command from the terminal.
```bash
docker build -t test:pandas .
```
The following command pulls the docker image from the cloud.
```bash
docker pull dpage/pgadmin4
``` 
Running the `postgres:13` image. Searches for the image locally first, if not available then pulls the image from the dockerhub.
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```
* `-e` : Defines the environment variable.
* `-v` : Defines the volume(_very important for storing data permanently_) 
* `-p` : Defines the port.

Connecting the postgresql database and using from the command line we need a pgcli module.
```bash
pip install pgcli
# After installing the `pgcli` module run the following command in terminal
pgcli -h localhost -p 5432 -u root -d ny_taxi
```
* `-h` : Defines the host/server name or address.
* `-p` : Defines the post.
* `-u` : Defines the username of the database.
* `-d` : Defines the name of the database.

The dataset we are gonna be use on this zoomcamp can be found from the given link:
* [Link1](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
* [Link2](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet)

Running `pgadmin` from the docker image. To interact with the previous running database:
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```
For successful interaction between containers the container needs to be on same network. If the `pgdatabase` & `pgadmin` needs to interact they must be on same network. To create a network we can run the following command.
```bash
  docker network create <network_name>
  # Eg. docker network create pg-network
```
Now for running the `postgres:13` image on a pre-defined network we need to add `--network=pg-network` arguments while running container.
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```
_Note: For successful connection define the `--name` for the container as well._

Now running `pgadmin` container on a pre-defined network.
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pg-admin4 \
  dpage/pgadmin4
```
If all things goes right then we can create a `docker-compose.yaml` file which would automatically run the both images in a single network.
The sample for the `docker-compose.yaml` file is:
```docker
services:
  pgdatabase:
    image: postgres:13
    environment:
      - POSTGRES_PASSWORD=root
      - POSTGRES_DB=ny_taxi
      - POSTGRES_USER=root
    volumes:
      - "./ny_taxi_postgres_data:/var/lib/postgresql/data:rw"
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@admin.com
      - PGADMIN_DEFAULT_PASSWORD=root
    ports:
      - "8080:80"
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

**This command is very useful to converting the jupyter notebook files to python script.**
```bash
jupyter nbconvert --to=script upload-data.ipynb
```  
The url for our dataset: 
[LINK]("https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.csv")

For inserting data to our previous running database we have prepared a following script.
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
Running the script for writing data to the database table:
```bash
python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url="http://172.17.0.1:8000/yellow_tripdata_2021-01.csv"
```
_Note: url is given from the local server._

For creating local server we can use the following command.
```bash
python-m http.server
```
_Now we can open our local server from `http://localhost:8080`_

If all things goes fine then we can create a image of our python script for data ingestion. Sample for the docker file can be:
```docker
FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_data.py ingest_data.py


ENTRYPOINT [ "python", "ingest_data.py" ]
```
Write the following command in terminal to create a docker image.
```bash
docker build -t taxi_ingest:v001 .
```
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
