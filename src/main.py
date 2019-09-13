import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/mnt/c/Users/aleja/Documents/llaves/tlac-vision/tlac-vision-c0786b53c370.json"
os.environ['bkt_todo'] = "tlac-book-covers-todo"
os.environ['bkt_done'] = "tlac-book-covers-done"
os.environ['bkt_failed'] = "tlac-book-covers-failed"
os.environ['book_table'] = "book_inventory"
os.environ['error_table'] = "failed_books"
os.environ['dataset_name'] = "book_backend"

from bigquery_script import load_book_from_ndjson
from book_api_script import search_query, construct_json_query
from storage_script import list_blobs, move_blob
from vision_script import parse_vision_description
from utils import format_q_search, write_ndjson_file, write_ndjson_error_file

bkt_todo = os.environ.get('bkt_todo')
bkt_done = os.environ.get('bkt_done')
bkt_failed = os.environ.get('bkt_failed')
book_table = os.environ.get('book_table')
error_table = os.environ.get('error_table')

import re 

def process_front_cover():
    if list_blobs(bkt_todo) != []:
        for cover in list_blobs(bkt_todo):
            if re.search('^.*[.]1[.].*',cover):
                try:
                    cover_text = parse_vision_description(cover)
                    cover_text = format_q_search(cover_text)
                    bjson = construct_json_query(cover_text)
                    print(cover)
                    #write_ndjson_file(bjson)
                    #load_book_from_ndjson(book_table)
                except Exception as e:
                    pass
                    #write_ndjson_error_file(cover, str(e))
                    #load_book_from_ndjson(error_table)
                    #move_blob(bkt_todo, cover, bkt_failed, cover)
                else:
                    pass
                    #move_blob(bkt_todo, cover, bkt_done, cover)
    else:
        print("no results")

process_front_cover()


