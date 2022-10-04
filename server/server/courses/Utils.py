import json
from django.core import serializers


def BodyData(request):
    content = None
    if request.body:
        content = json.loads(request.body.decode('utf-8'))
    return content


def ModelToJson(model):
    return json.loads(serializers.serialize('json', [model, ]))[0]['fields']
