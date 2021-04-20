web: gunicorn -b 0.0.0.0:$PORT cactusco.wsgi
worker: celery -A cactusco worker -l INFO 