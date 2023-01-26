import functools

from flask import (
    Blueprint, flash, g, render_template, request, session, url_for
)

from search.opensearch import get_os_client

bp = Blueprint('search', __name__)


@bp.route('/', methods=['GET'])
def home():
  if request.method == 'GET':
    pass

  return render_template('search/search.html')


@bp.route('/search', methods=['POST'])
def search():
  error = None
  query = request.form['query']


  if len(query) == 0:
    error = "Please enter a search"

  if error is None:
    data = __search(query)
    return render_template("results/results.html", results=data)

  flash(error)


@bp.route('/typeahead', methods=['POST'])
def typeahead():
  typeahead_templates = {
      "completion": __completion(),
      "search_as_you_type": __search_as_you_type()
  }

  template = typeahead_templates.get(request.args.get(
      'typeahead-type', default='completion', type=str), 'completion')
  error = None
  curr_search = request.form['typeahead']
  if not type(curr_search) == str:
    raise TypeError("curr_search is not of type string")

  if len(curr_search) > 0:
    results = g.opensearch.search(template(querystring=curr_search))
    # Typeahead query
    pass


def __search(query):
  client = get_os_client()
  query = {
    "query": {
      "multi_match": { 
        "query": query,
        "fields": [
            "title",
            "overview",
        ]
      }
    }
  }
  results = client.search(index="movie-metadata", body=query)
  return results["hits"]["hits"]


def __search_as_you_type():
  def template(querystring: str):
    if not type(querystring) == str:
      raise TypeError("querystring is not of type string")
    return {
        "query": {
            "multi_match": {
                "query": querystring,
                "type": "bool_prefix",
                "fields": [
                    "search-as-you-type",
                    "search-as-you-type._2gram",
                    "search-as-you-type._3gram"
                ]
            }
        }
    }
  return template


def __completion():
  def template(querystring: str):
    if not type(querystring) == str:
      raise TypeError("querystring is not of type string")
    return {
        "suggest": {
            "movie-suggestions": {
                "prefix": querystring,
                "completion": {
                    "field": "completion"
                }
            }
        }
    },
  return template
