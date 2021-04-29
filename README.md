
# Cactus Computing Product Recommendation Sotfware for eCommerce
_This codebase is no longer mantained_

This is Cactus Computing Cross-Selling and Up-Selling software which is now open sourced. The documentation is a little messy and you should use it at your own risk.

## What does this repository do

This is an implementation of cross-selling and up-selling product recommendation generation algorithms, API and frontend carrousels. 

## How it works

We build an API to serve the models by selecting the top-k closest recommendation for a given product and company. This API is feed from a prediction database which is updated daily through the scripts in `products/scripts`.

The way to integrate with the sites frontend is thorugh a Google Tag Manager Custom Tag. You need to insert this script, replacing example.com with your own host.

```html
<script src="https://example.com/cactusScript.js">
```


The code in `cactusScript.js` is plain vanilla javascript and all it does is generate the necesary html to create the carrousel and import the styles for every customer. The styling specific to each customer need to be changed for each one of them manually. 

Bellow you will find the instructions necessary to run this application in a dev environment and how we used it in production (we know it's a little messy but we hope it helps!).

## Index:

- [Runnig Dev Envirnoment](##runnig-dev-envirnoment)
- [Dev Environment Setup](##dev-environment-setup)
- [Prod Environment Setup](##prod-environment-setup)
- [Deploy](##deploy)
- [Useful commands](##useful-commands)
- [How to drop all public tables on DB. ](##how-to-drop-all-public-tables-on-db. )
- [Integrations](##integrations)
- [Django scripts](##django-scripts)
- [API Documentation](##api-documentation)
- [Google Tag Manager (GTM)](##google-tag-manager-(gtm))
- [Django Linting](##django-linting)

## Environment Variables

The following environment variables are required for the application to work. A file is created `.env-dev` as a template for you to fill up. You need to change its name to `.env` for it to work locally. Here is a description of each variable

```
SECRET_KEY: Django Secret Key
GOOGLE_APPLICATION_CREDENTIALS: Path to your GCP Service Account key
EMAIL_HOST_USER: this is an email account to send emails from the landing page contact form
EMAIL_HOST_PASSWORD: You need to create a passwork from the google application credentials panel in order for this to work
DATABASE_URL: database url as per sqlalchemy
DEBUG: true/false
HOST: allowed host
NGROK_AUTHTOKEN: you need an ngrok account for this. Its only used to tunnel your local changes to a Google Tag Manager tag for developing purposes
REDIS_TLS_URL: Redis URL
REDIS_URL: Redis URL
```

## Dev Environment Setup

Clone the repository
```
git clone https://github.com/vescobarb/MVP_inventory.git cactusco
```

Download/Get credentials. You need a `.env` file which contains secret configuration parameters. Talk to the administrator if you do not have gcloud premissions.

```
gsutil cp gs://cactus-stockapp/credentials/.env-dev ./cactusco/.env
gsutil cp gs://cactus-stockapp/credentials/service_account_key.json ./cactusco/service_account_key.json
```
Create containers
```
docker-compose up
```
To add models to database:

```
docker-compose run web /usr/local/bin/python manage.py migrate
```

- [Index](##index)
## Runnig Dev Envirnoment

To build your local environment in docker run
```
docker-compose up --build
```

Download/Get credentials. You need a `.env` file which contains secret configuration parameters. Talk to the administrator if you do not have gcloud premissions.

```
gsutil cp gs://cactus-stockapp/credentials/.env-dev ./cactusco/.env
gsutil cp gs://cactus-stockapp/credentials/service_account_key.json ./cactusco/service_account_key.json
```
- [Index](##index)
## Prod Environment Setup

Ubuntu 18.04

Clone the repository

```
sudo git clone https://github.com/vescobarb/MVP_inventory.git cactusco
```

Move to stockapp directory

Download/Get credentials. You need a `.env` file which contains secret configuration parameters. Talk to the administrator if you do not have gcloud premissions.

```
sudo gsutil cp gs://cactus-stockapp/credentials/.env ./cactusco/.env
sudo gsutil cp gs://cactus-stockapp/credentials/service_account_key.json ./cactusco/service_account_key.json
```

```
sudo apt update 
sudo apt install software-properties-common
```
```
sudo add-apt-repository ppa:deadsnakes/ppa 
```
```
sudo apt update 
sudo apt install python3.9
```
```
python3.9 -V 
```
Move to ```/usr/local/stockapp```

install pip, nginx:

```
sudo apt update -y
sudo apt install python3-pip python3-dev libpq-dev nginx curl -y
```

Install virtualenv
```
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
```

Create a user and give permissions:

```
sudo adduser cactus --disabled-login --disabled-password --gecos "cactus system user"
sudo chown cactus.cactus . -R
sudo chmod g+rwx . -R
sudo su cactus
```

Create and activate
```
virtualenv .venv
source .venv/bin/activate
```
Install requirements
```
.venv/bin/python3 -m pip install -r requirements.txt
```
you should be ready to deploy:

```
gunicorn --bind 0.0.0.0:8000 cactusco.wsgi
```
Exit stockapp user to do sudo operations
Move systemd socket file:
```
sudo cp deploy_files/gunicorn.socket /etc/systemd/system/gunicorn.socket
```
Move systemd service file

```
sudo cp deploy_files/gunicorn.service /etc/systemd/system/gunicorn.service
```

Now we init and enable systemd:

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

Verify the systemd status:
```
sudo systemctl status gunicorn.socket
journalctl -xe
```
Test your socket activation
```
curl --unix-socket /run/gunicorn.sock localhost
sudo systemctl status gunicorn.socket
```
if any change is needes, change it and reload socket:
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```

Cofigure Nginx for auth pass for gunicorn
move
```
sudo cp deploy_files/cactusco /etc/nginx/sites-available/cactusco
```

Now we can habilitar the file binding it to site-enable directory
```
sudo ln -s /etc/nginx/sites-available/cactusco /etc/nginx/sites-enabled
```

Test the config:
```
sudo nginx -t
```
if anything goes wrong we can check files and then restar nginx:
```
sudo systemctl restart nginx
```
Then we change url:
```
sudo nano /etc/nginx/sites-available/cactusco
```
under server name we change the IP to ```www.cactusco.cl```
then on .env:
```
sudo nano cactusco/.env
```
under HOST we change the IP to ```www.cactusco.cl```
Here we have to go to Cloud DNS and point our domain to the instance external IPs

Finnaly we open our firewall to the normal traffict of 80 port:
```
sudo ufw delete allow 8000
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

Now we SSL our url

first move usr/ and the run this command
```
sudo add-apt-repository ppa:certbot/certbot
```
Install certbot
```
sudo apt install python-certbot-nginx
```
Now we certify our domain
```
sudo certbot --nginx -d www.cactusco.cl -d cactusco.cl
```
Then reload nginx
```
sudo systemctl reload nginx
```
- [Index](##index)

## Deploy:
### Dev:
```
cd /usr/local/CactusCo
sudo git pull origin <branch name> dev
sudo su cactus
source .venv/bin/activate
python manage.py collectstatic
exit
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```
### Prod:
```
cd /usr/local/cactusco
sudo git pull origin <branch name> main
sudo su cactus
source .venv/bin/activate
python manage.py collectstatic
exit
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

- [Index](##index)
## Useful commands
```
docker-compose run web /usr/local/bin/python manage.py makemigrations stockapp
```

```
docker-compose run web /usr/local/bin/python manage.py migrate
```

Resets migrations
```
docker-compose run web /usr/local/bin/python manage.py migrate api zero
```

To connect to the app shell

```
docker-compose run web /usr/local/bin/python manage.py shell
```

Creating an admin user

```
docker-compose run web /usr/local/bin/python manage.py createsuperuser
```
- [Index](##index)
## How to drop all public tables on DB. 

This is necesary when making structural changes to the database, which should be avoided. If you must do such structural changes, please discuss the changes with the team beforehand.
First, ssh postgres container
```
docker exec -it <containername> bash
```
Login to database
```
psql -U postgres
```
Drop tables
```
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```
¡You are done! You can now migrate your changes to the db.
- [Index](##index)
## Integrations

Integrations are the set of scripts we use to connect to online stores such as Shopify or Magento. We will use them as scripts for the moment but eventually we'll automate them.

### Requirements

Aside from the package requirements, you need to download the API credentials for the integrations. You need to have installed the GC SDK.

```
gsutil cp gs://cactus-landing/credentials/.shopify-env ./integrations/shopify/.shopify-env
gsutil cp gs://cactus-landing/credentials/magento-keys.json ./scripts/magento/magento-keys.json
gsutil cp gs://cactus-landing/credentials/wc-keys.json ./scripts/wc/wc-keys.json
```

It is recommendend to create a virtualenv and install package requirements in it

```
source activate .venv
pip install -r requirements.txt
```

### Uploading user product to ecommerce.cactusco.cl

Delete all products
```
docker-compose run web /usr/local/bin/python ./integrations/woocommerce/upload_product_test.py <company name> delete_prod
```
Create all products
Download products from ecommerce.cactusco.cl
```
docker-compose run web /usr/local/bin/python ./integrations/woocommerce/wc.py cactus get_data
```
Upload related products to ecommerce.cactusco.cl
```
docker-compose run web /usr/local/bin/python ./integrations/woocommerce/upload_product_test.py <company name> related_prod
```
- [Index](##index)
## Django scripts
### Get products

sudo docker run --rm cactusco /usr/local/bin/python manage.py runscript predict_cross_sell --script-args pippa

sudo docker run --rm cactusco /usr/local/bin/python manage.py runscript predict_up_sell --script-args pippa

- [Index](##index)
## API Documentation

The API exposes the cross selling products for a given `product_id` and `company` name. 

To test this, you must upload test data to the database.
To test cross_selling
```
http://localhost:8000/api/cross_selling?name=kit impresora 3d tarjeta controladora ramps 1.4 arduino mega&company=makerschile&top-k=4
http://localhost:8000/api/cross_selling?name=PMG - Karma&company=quema&top-k=4
```
To test up_selling

```
http://localhost:8000/api/up_selling?name=kit impresora 3d tarjeta controladora ramps 1.4 arduino mega&company=makerschile&top-k=4
http://localhost:8000/api/up_selling?name=PMG - Karma&company=quema&top-k=4
```
- [Index](##index)
## Google Tag Manager (GTM)
cookie_related_product_clicked.js crea una cookie cada vez que un usuario hace click en una sección de productos relacionados de Prat, esa cookie dura 5 días.
Obs: para cada eCommerce hay que cambiar la clase CSS de sección de productos relacionados hasta que tengamos nuestro script de front de carrousel de productos relacionados

cookie_related_product_amount_purchased.js 
1. Compara el nombre de cada producto comprado con los nombre de cookies de productos relacionados con click, si es que hay un producto comprado que fue marcado como "relacionado", entonces suma el valor de la compra de ese producto.

2. Crea una cookie con el monto total de productos relacionados, esa cookie es luego leida por una variable de GTM y enviada a Google Analytics (GA).
Obs: Para cada eCommerce hay que cambiar como se leen los productos comprados

### Resumen Proceso:

1. Se crea una cookie por cada producto relacionado en el que el cliente hace click
2. En la página de "Gracias por su Compra" pasan los siguientes eventos:
    1. Se leen todos los productos comprados
    2. Se comparan con los productos relacionados con click
    3. Se suman los montos de esos productos y se crea una cookie con el monto total
    4. Se lee esa cookie desde una variable en GTM
    5. Se envía un evento a GTM con el valor de la variable (monto total comprado de productos relacionados)
    6. Se elimina la cookie del monto total


- [Index](##index)

## Django Linting

To use pylint-django to inspect your code, run the following command

```
docker-compose run web /usr/local/bin/python -m pylint --load-plugins pylint_django <file_name_or_path_name>
```

This will point out posible conventions that are not being followed in your code. Also it will point out any errors.


- [Index](##index)


## Ngrok

[Ngrok docs](https://ngrok.com/docs)

This is the setup of ngrok to route traffic through a custom domain name.

To tunnel the traffic from `http://demo.cactusco.cl/` to your local machine, you need to install ngrok

```
brew install --cask ngrok
```

Then, you must authenticate using

```
ngrok authtoken <auth-token>
```

You can find the authtoken in the `.env` file of the project (check out the [Dev Environment Setup](##dev-environment-setup) section to get the file). From the `.env` file copy your authtoken for the ngrok service.

Then, use the `--hostname` when serving your files

```
ngrok http -hostname=demo.cactusco.cl <server-port>
```

If you want to add another domain to the allowed hosts, you must first set up your new domain [here](https://dashboard.ngrok.com/endpoints/domains). Then, you must add the domain to your HOST parameter in the .env file inside `/cactusco`.

## Javascript
 
### ESLint
You have to install npm.

```
brew install npm
```

Once that's done, install node dependencies by running

```
npm install
```
You may need to enable ESLint in VSCode by going into a JS file, in the firstline there will be a warning highlight. Click on it and a small lightbulb will apear. Click on the lightbulb to enable the linter.


Celery:
1. Check redis-server status:
```
sudo systemctl status redis-server
```
2. Start cactusco-app

3. Start celery worker:
```
celery -A cactusco worker -l INFO --purge
```

To run the tasj you have to call this endpoint:
```
http://localhost:8000/products/get_products
```
The output would be a list of tasks ids that you need to keep to check on the tasks status in this endpoint:
```
http://localhost:8000/products/check_status?task_id=5fe7da16-19aa-4fe7-a463-4580dc811193
```

## Django Debugging

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'mysite.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'MYAPP': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
    }
}
```
