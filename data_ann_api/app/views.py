import json

from django.conf import settings
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.shortcuts import render
from app.models import ImageRef

from django.http import HttpResponse
"""
{
  "messages": [
    {
      "attachment": {
        "type": "image",
        "payload": {
          "url": "BASE_URL/IMAGE_ID"
        }
      }
    },
    {
      "attachment": {
        "type": "template",
        "payload": {
          "template_type": "button",
          "text": "Is it a car or not?",
          "buttons": [
            {
              "url": "BASE_URL/?image=IMAGE_ID&label=car&user=USER_ID",
              "type":"json_plugin_url",
              "title":"Car"
            },
            {
              "url": "BASE_URL/?image=IMAGE_ID&label=not_car&user=USER_ID",
              "type":"json_plugin_url",
              "title":"Not a car"
            }
          ]
        }
      }
    }
  ]
}
"""
def create_json_response(image_url, image_id, user_id):
    template = {
      "messages": [
        {
          "attachment": {
            "type": "image",
            "payload": {
              "url": image_url
            }
          }
        },
        {
          "attachment": {
            "type": "template",
            "payload": {
              "template_type": "button",
              "text": "Is it a car or not?",
              "buttons": [
                {
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=car&messenger+user+id={user_id}',
                  "type":"json_plugin_url",
                  "title":"Car"
                },
                {
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=not_car&messenger+user+id={user_id}',
                  "type":"json_plugin_url",
                  "title":"Not a car"
                },
                {
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=unlabeled&messenger+user+id',
                  "type":"json_plugin_url",
                  "title":"I can't decide"
                }
              ]
            }
          }
        }
      ]
    }
    return template


def chat_request(request):
    if 'messenger user id' in request.GET and not 'image' in request.GET:
        instance: ImageRef = ImageRef.objects.filter(user_id__isnull=True).first()
        if not instance:
            return HttpResponse(json.dumps({"messages": [{"text": "Missing images ;("}]}), status=400)
        json_response = create_json_response(instance.image_url, instance.id, request.GET['messenger user id'])
    elif 'messenger user id' in request.GET and 'image' in request.GET and 'label' in request.GET:

        image_id = request.GET['image']
        user_id = request.GET['messenger user id']
        label = request.GET['label']
        try:
            instance = ImageRef.objects.get(id=image_id)
        except ImageRef.DoesNotExist:
            return HttpResponse(
                json.dumps({"messages": [{"text": "Missing images ;("}]}), status=400)
        instance.user_id = user_id
        instance.label = label
        instance.save()
        new_instance: ImageRef = ImageRef.objects.filter(
            user_id__isnull=True).first()
        if not instance:
            return HttpResponse(json.dumps({"messages": [{"text": "Missing images ;("}]}), status=400)
        json_response = create_json_response(new_instance.image_url, new_instance.id, user_id)
    else:
        return HttpResponse(json.dumps({'error': 'Missing parameters'}), status=400)
    return HttpResponse(json.dumps(json_response),
                        content_type="application/json")


def list_labels(request):
    queryset = ImageRef.objects.filter(label__isnull=False)
    raw_data = serializers.serialize('python', queryset, fields=('image_url', 'label'))
    actual_data = [d['fields'] for d in raw_data]
    return HttpResponse(json.dumps(actual_data), content_type="application/json")
