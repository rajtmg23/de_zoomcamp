### Start by Cloning the repo:
```shell
git clone https://github.com/mage-ai/mage-zoomcamp.git mage-zoomcamp
```
### Navigate to the repo:
```shell
cd mage-data-engineering-zoomcamp
```
Rename `dev.env` to simple `.env` --This contains the environment variable needed for the project.

Now, Let's build the container:
```shell
docker compose build
```
For getting the latest update, we can use the following command:
```shell
docker pull mageai/mageai:latest
```
Everything is setup. Now we can start the container:
```shell
docker-compose up
```
Now, navigate to http://localhost:6789 in your browser! Voila! You're ready to get started.
