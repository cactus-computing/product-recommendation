# MVP_inventory

# Runnig Dev Envirnoment

```
docker-compose up --build
```

# Dev Environment Setup

Clone the repository
```
git clone https://github.com/vescobarb/MVP_inventory.git
```

Download/Get credentials. You need a `.env` file which contains secret configuration parameters. Talk to the administrator if you do not have gcloud premissions.

```
gsutil cp gs://cactus-stockapp/credentials/.env ./invetory_test/
gsutil cp gs://cactus-stockapp/credentials/service_account_key.json ./inventorymvp/
```

then run the following command to start a django project

```
docker-compose run web django-admin startproject inventory_test .
```

then create the containers

```
docker-compose up
```

then from an other terminal (because app is running on the frist one)

```
docker-compose run web django-admin startapp myapp
```

add the following lines to inventory_test/settings.py under ``` BASE_DIR = Path(__file__).resolve().parent.parent ```

```
MEDIA_URL = '/documents/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'documents')
To migrate the app to a Data Base
```

Inside INSTALLED_APPS paste this:
```
'myapp',
'crispy_forms',
```
Inside
``` 
TEMPLATES = [
    ...
        'OPTIONS': {
            'context_processors':
```
paste:
```
'django.template.context_processors.media',
```
Replace urlpatterns whit this:
```
urlpatterns = [
    path('', include('myapp.urls')),
    path('admin/', admin.site.urls),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

To add models to database:

```
docker-compose run web /usr/local/bin/python manage.py makemigrations inventorymvp
```

```
docker-compose run web /usr/local/bin/python manage.py migrate
```

To connect to the app shell

```
docker-compose run web /usr/local/bin/python manage.py shell
```
docker-compose run web /usr/local/bin/python manage.py rename_app myapp inventorymvp
Creating an admin user

```
docker-compose run web /usr/local/bin/python manage.py createsuperuser
```

