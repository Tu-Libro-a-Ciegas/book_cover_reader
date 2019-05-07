import json
from google.cloud import vision
from google.protobuf.json_format import MessageToJson
from storage_script import move_blob


def parse_vision_description(filename):
	client = vision.ImageAnnotatorClient()
	response = client.text_detection({'source': {'image_uri': 'gs://tlac-book-covers-todo/' + filename},})
	s_json = json.loads(MessageToJson(response))

	if s_json.get('textAnnotations') is not None:
		return s_json.get('textAnnotations')[0].get('description')
	else:
		raise Exception(f"Image {filename} did not contain text")

 