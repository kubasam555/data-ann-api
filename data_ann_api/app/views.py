import json

from django.core import serializers

from app.helpers import bot_error_message, bot_json_response
from app.models import ImageRef

from django.http import HttpResponse


def chat_request(request):
    if 'messenger user id' in request.GET and not 'image' in request.GET:
        instance: ImageRef = ImageRef.objects.filter(user_id__isnull=True).first()
        if not instance:
            return HttpResponse(
                bot_error_message('Missing new images ;('),
                status=400
            )
        json_response = bot_json_response(
            instance.image_url,
            instance.id,
            request.GET['messenger user id']
        )
    elif 'messenger user id' in request.GET and 'image' in request.GET and 'label' in request.GET:

        image_id = request.GET['image']
        user_id = request.GET['messenger user id']
        label = request.GET['label']
        try:
            instance = ImageRef.objects.get(id=image_id)
            instance.user_id = user_id
            instance.label = label
            instance.save()
        except ImageRef.DoesNotExist:
            return HttpResponse(
                bot_error_message('This image does not exists'),
                status=400
            )

        new_instance: ImageRef = ImageRef.objects.filter(
            user_id__isnull=True).first()
        if not instance:
            return HttpResponse(
                bot_error_message('Missing new images ;('),
                status=400
            )
        json_response = bot_json_response(
            new_instance.image_url,
            new_instance.id,
            user_id
        )
    else:
        return HttpResponse(
            bot_error_message('Missing parameters. Please, contact with admin'),
            status=400
        )
    return HttpResponse(
        json.dumps(json_response), content_type='application/json'
    )


def list_labels(request):
    queryset = ImageRef.objects.filter(label__isnull=False)
    raw_data = serializers.serialize(
        'python', queryset, fields=('image_url', 'label')
    )
    actual_data = [d['fields'] for d in raw_data]
    return HttpResponse(
        json.dumps(actual_data), content_type='application/json'
    )
