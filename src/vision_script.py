import json
from google.cloud import vision
from google.protobuf.json_format import MessageToJson
from storage_script import move_blob


def parse_vision_description(filename):
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(
        {'source': {'image_uri': 'gs://tlac-book-covers-todo/' + filename}, })

    # MessageToJson convierte la respuesta de Vision a JSON
    # json.loads convierte ese JSON en un dict para poder usarlo con python
    s_json = json.loads(MessageToJson(response))

    if s_json.get('textAnnotations') is not None:
        return s_json.get('textAnnotations')[0].get('description')
    else:
        return None
