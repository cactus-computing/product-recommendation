FROM python:3.8.8-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . /code/

RUN apt-get update 

RUN yes | apt-get install node

RUN yes | apt-get install npm

RUN npm install

RUN npm run build

CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "cactusco.wsgi"]

EXPOSE 8000