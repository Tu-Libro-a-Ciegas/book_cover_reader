import json
import requests


def search_query(query):
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=' + query + '&maxResults=5')
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        raise Exception(f"Response has status code of {response.status_code}")


jbook_dict = {}
jbook = search_query('MIGUEL DE CERVANTES+DON+QUIJOTE+DE LA MANCHA')
done = False
total_items = jbook.get('totalItems')

if total_items == 0:
    pass
    # no funciono
else:

    books = (item for item in jbook.get('items'))

    while done is False:

        current_book = next(books)

        desc = current_book.get('volumeInfo').get('description')
        if desc is not None and jbook_dict.get('description') is None:

            bid = current_book.get('id')
            tle = current_book.get('volumeInfo').get('title')
            stle = current_book.get('volumeInfo').get('subtitle')
            aut = current_book.get('volumeInfo').get('authors')

            jbook_dict.update({
                'description': desc,
                'id': bid,
                'title': tle,
                'subtitle': stle,
                'authors': aut})

        else:
            pass

        ctg = current_book.get('volumeInfo').get('categories')

        if ctg is not None:
            jbook_dict.update({'categories': ctg})
            done = True

        else:
            pass


print(jbook_dict)

# 'industryIdentifiers'

# 'maturityRating'
# 'previewLink'
# 'embeddable'
# 'textSnippet'