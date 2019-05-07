import os
from storage_script import list_blobs, move_blob
from vision_script import parse_vision_description

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/mnt/c/Users/Andres/Documents/api-keys/tlac-vision/tlac-vision-c0786b53c370.json"

bkt_todo = 'tlac-book-covers-todo'
bkt_done = 'tlac-book-covers-done'
bkt_failed = 'tlac-book-covers-failed'

for cover in list_blobs(bkt_todo):
	try:
		cover_text = parse_vision_description(cover)
	except:
		move_blob(bkt_todo, cover, bkt_failed, cover)
		#Log BQ
