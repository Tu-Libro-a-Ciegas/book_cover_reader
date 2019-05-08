import json
import requests


def search_query(query):
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + query + '&maxResults=5')
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception(f"Response has status code of {response.status_code}")
