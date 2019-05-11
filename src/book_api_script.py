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
        raise Exception(f'There where no results for the query: {query}')
    else:
        books = (item for item in jbook.get('items'))
        while done is False:
            try:
                current_book = next(books)
            except StopIteration:
                if jbook_dict.get('description') is None:
                    raise Exception(f'There where no available descriptions for the query: {query}')
                else:
                    done = True

            desc = current_book.get('volumeInfo').get('description')
            if desc is not None and jbook_dict.get('description') is None:

                bid = current_book.get('id')
                tle = current_book.get('volumeInfo').get('title')
                stle = current_book.get('volumeInfo').get('subtitle')
                auts = str(current_book.get('volumeInfo').get('authors'))
                matu = current_book.get('volumeInfo').get('maturityRating')
                prev = current_book.get('volumeInfo').get('previewLink')
                emb = current_book.get('accessInfo').get('embeddable')
                iids = str(current_book.get('volumeInfo').get('industryIdentifiers'))

                if current_book.get('searchInfo') is not None:
                    snpt = current_book.get('searchInfo').get('textSnippet')
                else:
                    snpt = None

                jbook_dict.update({
                    'description': desc,
                    'id': bid,
                    'title': tle,
                    'subtitle': stle,
                    'authors': auts,
                    'maturity': matu,
                    'preview_link': prev,
                    'embeddable': emb,
                    'industry_identifiers': iids,
                    'snippet': snpt})

            else:
                pass

            ctg = current_book.get('volumeInfo').get('categories')

            if ctg is not None:           
                if current_book.get('searchInfo') is not None and jbook_dict.get('snippet') is None:
                    snpt = current_book.get('searchInfo').get('textSnippet')
                else:
                    snpt = None

                jbook_dict.update({
                    'categories': ctg,
                    'snippet': snpt})
                

            else:
                jbook_dict.update({'categories': None})
    
    return jbook_dict
