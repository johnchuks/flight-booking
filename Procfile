web: gunicorn config.wsgi --log-file -
worker: celery -A TASKFILE worker -B --loglevel=info