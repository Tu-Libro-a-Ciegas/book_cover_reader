import os
from bigquery_script import load_book_from_ndjson
from book_api_script import search_query, construct_json_query
from storage_script import list_blobs, move_blob
from vision_script import parse_vision_description
from utils import format_q_search, write_ndjson_file


bkt_todo = 'tlac-book-covers-todo'
bkt_done = 'tlac-book-covers-done'
bkt_failed = 'tlac-book-covers-failed'

for cover in list_blobs(bkt_todo):
	try:
		cover_text = parse_vision_description(cover)
		cover_text = format_q_search(cover_text)
		print(cover_text)
		bjson = construct_json_query(cover_text)
		write_ndjson_file(bjson)
		load_book_from_ndjson()

	except Exception as e:
		print(e)
		move_blob(bkt_todo, cover, bkt_failed, cover)
		# Log BQ
	else:
		move_blob(bkt_todo, cover, bkt_done, cover)
