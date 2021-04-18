FROM python:3.8.8-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt update

RUN apt install redis-server -y

COPY requirements.txt /code/

COPY requirements-ia.txt /code/

RUN pip install -r requirements.txt

RUN pip install -r requirements-ia.txt

RUN celery -A cactusco worker -l INFO

COPY . /code/

CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "cactusco.wsgi"]

EXPOSE 8000