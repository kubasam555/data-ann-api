import json

from django.conf import settings
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
              "url": f'{settings.BACKEND_URL}{image_url}'
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
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=car&user={user_id}',
                  "type":"json_plugin_url",
                  "title":"Car"
                },
                {
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=not_car&user={user_id}',
                  "type":"json_plugin_url",
                  "title":"Not a car"
                },
                {
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=unlabeled&user={user_id}',
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
    if 'user' in request.GET and not 'image' in request.GET:
        qs: ImageRef = ImageRef.objects.filter(user_id__isnull=True).first()
        json_response = create_json_response(qs.image_url, qs.id, request.GET['userId'])
    elif 'user' in request.GET and 'image' in request.GET and 'label' in request.GET:

        image_id = request.GET['image']
        user_id = request.GET['user']
        label = request.GET['label']
        instance = ImageRef.objects.get(id=image_id)
        instance.user_id = user_id
        instance.label = label
        instance.save()
        json_response = create_json_response(instance.image_url, instance.id, user_id)
    else:
        return HttpResponse(json.dumps({'error': 'Missing parameters'}), status=400)
    return HttpResponse(json.dumps(json_response),
                        content_type="application/json")


