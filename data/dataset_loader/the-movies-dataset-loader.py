from os import pathpre
import pandas as pd
from util import to_opensearch, to_ndjson, get_os_client
from ast import literal_eval
import json


def json_formatter(data):
  """Used to solve for nan data in json fields"""
  if pd.isnull(data):
    return None
  return literal_eval(data)


def ingest_data():
  dataframe = pd.read_csv(path.join(
      '.', 'data', 'datasets', 'the-movies-dataset', 'movies_metadata.csv'))

  dataframe["genres"] = dataframe["genres"].apply(json_formatter)
  dataframe["production_companies"] = dataframe["production_companies"].apply(
      json_formatter)
  dataframe["production_countries"] = dataframe["production_countries"].apply(
      json_formatter)
  dataframe["spoken_languages"] = dataframe["spoken_languages"].apply(
      json_formatter)

  formatted_data = dataframe.to_json(orient='records')

  bulk_data = []
  for item in json.loads(formatted_data):
    tmp_item = {
        **item, "completion": [item['title']], "search-as-you-type": item['title']}
    bulk_data.append(
        {"index": {"_index": "movie-metadata", "_id": item['id']}})
    bulk_data.append(tmp_item)

  to_opensearch(to_ndjson(bulk_data))


def create_index_template():
  os_client = get_os_client()
  if os_client.indices.exists_index_template("movie-metadata"):
    os_client.indices.delete_index_template("movie-metadata")

  body = {
      "index_patterns": [
          "movie-metadata*"
      ],
      "template": {
          "settings": {
              "analysis": {
                  "analyzer": {
                      "text_analyzer": {
                          "tokenizer": "standard",
                          "filter": ["stop"]
                      }
                  }
              }
          },
          "mappings": {
              "properties": {
                  "completion": {
                      "type": "completion"
                  },
                  "search-as-you-type": {
                      "type": "search_as_you_type"
                  },
                  "release_date": {
                      "type": "date",
                  }
              }
          }
      }
  }
  os_client.indices.put_index_template("movie-metadata", body=body)


if __name__ == "__main__":
  import util
  import logging
  logger = logging.getLogger('dataset-loader')
  util.init_logging(logger, 'DEBUG')
  util.initialize_opensearch_client(
      {"hosts": ["https://admin:admin@localhost:9200"],  # pragma: allowlist secret
       "use_ssl": True,
       "verify_certs": False,
       "ssl_show_warn": False}
  )
  create_index_template()
  ingest_data()
