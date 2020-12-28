# MVP_inventory

## Frist clone the repository

```
git clone https://github.com/vescobarb/MVP_inventory.git
```
## To create from scratch

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

## If everything is created, just start docker container

```
docker-compose up
```


