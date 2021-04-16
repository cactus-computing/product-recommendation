FROM python:3.8.8-buster
# create and set working directory
RUN mkdir /CactusCo
WORKDIR /CactusCo

# Add current directory code to working directory
ADD . /CactusCo/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8000
ENV SECRET_KEY=${{ secrets.CACTUS_SECRET_KEY }}
ENV EMAIL_HOST_USER=${{ secrets.DJANGO_EMAIL_HOST_USER }}
ENV EMAIL_HOST_PASSWORD=${{ secrets.DJANGO_EMAIL_HOST_PASSWORD }}
ENV DATABASE_URL=${{ secrets.DJANGO_DATABASE_URL }}
ENV DEBUG=${{ secrets.CACTUS_DEBUG }}
ENV HOST=${{ secrets.CACTUS_HOST }}
ENV NGROK_AUTHTOKEN=${{ secrets.NGROK_AUTHTOKEN}}
 
# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        tzdata \
        python3-setuptools \
        python3-pip \
        python3-dev \
        python3-venv \
        git \
        && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip 
RUN pip3 install pipenv

# Install project dependencies
RUN pipenv install --skip-lock --system --dev

EXPOSE 8000
CMD gunicorn cactusco.wsgi:application --bind 0.0.0.0:$PORT