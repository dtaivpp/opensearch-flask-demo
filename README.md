flask --app search --debug run

kaggle datasets download -d rounakbanik/the-movies-dataset -p data/datasets
tar xzf data/datasets/the-movies-dataset.zip -C data/datasets