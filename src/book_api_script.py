import json
import requests


def search_query(query):
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + query + '&maxResults=5')
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception(f"Response has status code of {response.status_code}")


def construct_json_query(query):
    jbook_dict = {}
    jbook = search_query(query)
    done = False
    total_items = jbook.get('totalItems')

    if total_items == 0:
        # raise Exception(f'There where no results for the query: {query}')
        jbook_dict.update({
                    'description': None,
                    'title': None,
                    'subtitle': None,
                    'authors': None,
                    'categories': None})
    else:
        books = (item for item in jbook.get('items'))
        while done is False:
            try:
                current_book = next(books)
            except StopIteration:
                done = True
                # if jbook_dict.get('description') is None:
                #     raise Exception(f'There where no available descriptions for the query: {query}')
                # if jbook_dict.get('categories') is None:
                #     raise Exception(f'There where no available categories for the query: {query}')

            desc = current_book.get('volumeInfo').get('description')
                        
            if desc is not None and jbook_dict.get('description') is None:
                tle = current_book.get('volumeInfo').get('title')
                stle = current_book.get('volumeInfo').get('subtitle')
                auts = current_book.get('volumeInfo').get('authors')
                ctg = current_book.get('volumeInfo').get('categories')

                jbook_dict.update({
                    'description': desc,
                    'title': tle,
                    'subtitle': stle,
                    'authors': auts,
                    'categories': ctg})
            else:
                pass

    return jbook_dict
