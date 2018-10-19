import json

from django.conf import settings


def bot_error_message(message):
    return json.dumps({"messages": [{"text": message}]})


def bot_json_response(image_url, image_id, user_id):
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
                  "type": "json_plugin_url",
                  "title": "Car"
                },
                {
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=not_car&messenger+user+id={user_id}',
                  "type": "json_plugin_url",
                  "title": "Not a car"
                },
                {
                  "url": f'{settings.BACKEND_URL}/image/?image={image_id}&label=unlabeled&messenger+user+id={user_id}',
                  "type": "json_plugin_url",
                  "title": "I can't decide"
                }
              ]
            }
          }
        }
      ]
    }
    return template
