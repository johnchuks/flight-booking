web: gunicorn config.wsgi --log-file -
worker: celery -A config worker --beat --loglevel=info