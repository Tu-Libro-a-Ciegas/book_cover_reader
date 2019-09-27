import json
import sys

def format_q_search(squery):
    return squery.rstrip().replace('\n', '+')


def format_q_search_with_spaces(squery):
    return squery.rstrip().replace('+', ' ')


def write_ndjson_file(response):
    if hasattr(sys, 'ps1'):
        with open('../temp/book_info.ndjson', 'w') as obj:
            obj.write(json.dumps(response))
    else:
        with open('temp/book_info.ndjson', 'w') as obj:
            obj.write(json.dumps(response))


def write_ndjson_error_file(file, err):
    response = format_error(file, err)
    with open('temp/book_error.ndjson', 'w') as obj:
        obj.write(json.dumps(response))


def format_error(file, err):
        return {'filename': file, 'error': err}
