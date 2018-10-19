release: python manage.py migrate --noinput
web: gunicorn --pythonpath data_ann_api data_ann_api.wsgi