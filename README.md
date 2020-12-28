# MVP_inventory

# Runnig Dev Envirnoment

```
docker-compose up
```

# Dev Environment Setup

```
git clone https://github.com/vescobarb/MVP_inventory.git
```
# First Time Run

```
docker-compose run web django-admin startproject inventory_test .
```

then 

```
docker-compose up
```

then from an other terminal (because app is running on the frist one)

```
docker-compose run web /usr/local/bin/python manage.py startapp front
```