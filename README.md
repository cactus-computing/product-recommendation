# MVP_inventory

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

## Useful commands


```
docker-compose run web /usr/local/bin/python manage.py makemigrations stockapp
```

```
docker-compose run web /usr/local/bin/python manage.py migrate
```

Resets migrations
```
docker-compose run web /usr/local/bin/python manage.py migrate landing zero
```

To connect to the app shell

```
docker-compose run web /usr/local/bin/python manage.py shell
```

Creating an admin user

```
docker-compose run web /usr/local/bin/python manage.py createsuperuser
```

How to drop all public tables on DB. This is necesary when making structural changes to the database, which should be avoided. If you must do such structural changes, please discuss the changes with the team beforehand.
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
