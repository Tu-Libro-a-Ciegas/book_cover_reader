import json


def format_q_search(squery):
    return squery.rstrip().replace('\n', '+')


def write_ndjson_file(response):
    with open('temp/book_info.ndjson', 'w') as obj:
        obj.write(json.dumps(response))
