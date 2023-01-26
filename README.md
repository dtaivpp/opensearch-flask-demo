flask --app search --debug run

kaggle datasets download -d rounakbanik/the-movies-dataset -p data/datasets
tar xzf data/datasets/the-movies-dataset.zip -C data/datasets


### Start the network observability example
docker compose --env-file ./deployments/network-observability/.env -f deployments/docker-compose.yml -f deployments/network-observability/docker-compose.fluent.yml
