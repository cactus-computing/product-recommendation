FROM python:3.8.8-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

COPY requirements-ia.txt /code/

RUN pip install -r requirements.txt

RUN pip install -r requirements-ia.txt

COPY . /code/

CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "cactusco.wsgi"]

EXPOSE 8000