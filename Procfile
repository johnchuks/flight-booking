web: gunicorn config.wsgi --log-file -
worker: celery worker -A config --loglevel=info
beat: celery -A config beat