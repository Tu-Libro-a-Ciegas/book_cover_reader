import os
import sys
import re 

if hasattr(sys, 'ps1'):
    try:
        os.chdir(os.path.join(os.getcwd(), 'src'))
    except FileNotFoundError:
        pass

from env_variables import *
from bigquery_script import load_book_from_ndjson, max_seq_id
from book_api_script import search_query, construct_json_query
from storage_script import list_blobs, move_blob
from vision_script import parse_vision_description
from utils import format_q_search, write_ndjson_file, write_ndjson_error_file, format_q_search_with_spaces

bkt_todo = os.environ.get('bkt_todo')
bkt_done = os.environ.get('bkt_done')
bkt_failed = os.environ.get('bkt_failed')
book_table = os.environ.get('book_table')
error_table = os.environ.get('error_table')

def process_front_cover():  ##borrar al final##
    if list_blobs(bkt_todo) != []:
        for cover in list_blobs(bkt_todo):
            if re.search('^.*[.]1[.].*',cover):
                try:
                    cover_text = parse_vision_description(cover)
                    cover_text = format_q_search(cover_text)
                    bjson = construct_json_query(cover_text)
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
                pass   

def update_book_inventory():

    if list_blobs(bkt_todo) != []:
        for cover in list_blobs(bkt_todo):
            if re.search('^.*[.]1[.].*',cover):
                ndj = {}
                mx_sq_id = max_seq_id()
                seq_id = (mx_sq_id + 1) if mx_sq_id is not None else 1
                manual_id = re.sub('.[0-9].jpeg', '', cover)
                cover_text = parse_vision_description(cover)
                if cover_text is not None:
                    cover_text = format_q_search(cover_text)
                    bjson = construct_json_query(cover_text)
                    
                    desc = bjson.get('description')
                    tle = bjson.get('title')
                    stle = bjson.get('subtitle')
                    auths = bjson.get('authors')
                    cats = bjson.get('categories')
                    cover_text = format_q_search_with_spaces(cover_text)
                    
                    if cats is not None:
                        status=2
                    else: 
                        status=None

            elif re.search('^.*[.]2[.].*',cover):
                bc_text = parse_vision_description(cover)

                if status is None:
                    if bc_text is not None:
                        status=1
                    elif bc_text is None and desc is not None:
                        status=1
                    elif bc_text is None and desc is None:
                        status=0
                    else:
                        pass
                
                ndj.update({
                "sequential_id": seq_id, 
                "manual_id": manual_id, 
                "title": tle, 
                "subtitle": stle, 
                "authors": auths, 
                "description": desc, 
                "categories": cats, 
                "cover": cover_text, 
                "back_cover": bc_text, 
                "status": status})

                write_ndjson_file(ndj)
                load_book_from_ndjson(book_table)

            else:
                pass 
            
    else:
        print("No books to process")

update_book_inventory()