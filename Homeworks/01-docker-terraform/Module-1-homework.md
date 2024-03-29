## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

`docker --help`

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

` Answer: --rm`
## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0

`Answer: 0.42.0 `

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```

You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)

**Code for writing data to the database.**
- [Jupyter Notebook File for storing zones data.](https://github.com/rajtmg23/de_zoomcamp/blob/main/01-docker-terraform/window_wsl_practice/docker/upload_zone_data.ipynb)
- [Jupyter Notebook File for storing green tripdata](https://github.com/rajtmg23/de_zoomcamp/blob/main/01-docker-terraform/window_wsl_practice/docker/upload_green_trip_data.ipynb)

## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612
- 15859
- 89009

`Answer: 15612`
```sql
SELECT COUNT(*) AS trip_count
FROM green_taxi_data gt
WHERE CAST(gt.lpep_pickup_datetime AS DATE) = '2019-09-18'
  AND CAST(gt.lpep_dropoff_datetime AS DATE) = '2019-09-18';
```

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

`Answer: 2019-09-26`
```sql
SELECT 
    CAST(lpep_pickup_datetime AS DATE), 
    MAX(trip_distance)
FROM
    green_taxi_data
GROUP BY CAST(lpep_pickup_datetime AS DATE)
ORDER BY 2 DESC LIMIT 1;
```


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

`Answer: "Brooklyn" "Manhattan" "Queens"`
```sql
SELECT
    tz."Borough" AS pickup_borough,
    SUM(gt.total_amount) AS total_amount
FROM
    green_taxi_data gt
JOIN
    taxi_zones tz ON gt."PULocationID" = tz."LocationID"
WHERE
    DATE(gt.lpep_pickup_datetime) = '2019-09-18'
    AND tz."Borough" != 'Unknown'
GROUP BY
    tz."Borough"
HAVING
    SUM(gt.total_amount) > 50000
ORDER BY
    total_amount DESC
LIMIT 3;
```

## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

`Answer: JFK Airport`

```sql
SELECT 
    tz_dropoff."Zone" AS dropoff_zone_name,
    MAX(gt.tip_amount) AS largest_tip_amount
FROM green_taxi_data gt
JOIN taxi_zones tz_pickup ON gt."PULocationID" = tz_pickup."LocationID"
JOIN taxi_zones tz_dropoff ON gt."DOLocationID" = tz_dropoff."LocationID"
WHERE TO_CHAR(gt.lpep_pickup_datetime, 'YYYY-MM') = '2019-09'
    AND tz_pickup."Zone" = 'Astoria'
GROUP BY tz_dropoff."Zone"
ORDER BY largest_tip_amount DESC
LIMIT 1;
```

## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.
