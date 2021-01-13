# MVP_inventory

## Runnig Dev Envirnoment

```
docker-compose up --build
```

Download/Get credentials. You need a `.env` file which contains secret configuration parameters. Talk to the administrator if you do not have gcloud premissions.

```
gsutil cp gs://cactus-stockapp/credentials/.env-dev ./invetory_test/.env
```

## Dev Environment Setup

Clone the repository
```
git clone https://github.com/vescobarb/MVP_inventory.git stockapp
```

Download/Get credentials. You need a `.env` file which contains secret configuration parameters. Talk to the administrator if you do not have gcloud premissions.

```
gsutil cp gs://cactus-stockapp/credentials/.env-dev ./invetory_test/.env
gsutil cp gs://cactus-stockapp/credentials/service_account_key.json ./inventorymvp/
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
git clone https://github.com/vescobarb/MVP_inventory.git stockapp
```

Move to stockapp directory

Download/Get credentials. You need a `.env` file which contains secret configuration parameters. Talk to the administrator if you do not have gcloud premissions.

```
gsutil cp gs://cactus-stockapp/credentials/.env ./invetory_test/
gsutil cp gs://cactus-stockapp/credentials/service_account_key.json ./inventorymvp/
```

Move to ```/usr/local/stockapp```

install pip, nginx:

```
sudo apt update
sudo apt install python3-pip python3-dev libpq-dev nginx curl
```

Install virtualenv
```
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
```

Create a user and give permissions:

```
sudo adduser stockapp --disabled-login --disabled-password --gecos "Stockapp system user"
sudo chown stockapp.stockapp . -R
sudo chmod g+rwx . -R
sudo su stockapp
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
gunicorn --bind 0.0.0.0:8000 invetory_test.wsgi
```
Exit stockapp user to do sudo operations
Move systemd socket file:
```
sudo mv /deployfiles/gunicorn.socket /etc/systemd/system/gunicorn.socket
```
Move systemd service file

```
sudo mv /deployfiles/gunicorn.service /etc/systemd/system/gunicorn.service
```

Now we init and enable systemd:

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

Verify the systemd status:
```
sudo systemctl status gunicorn.socket
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
sudo mv /deployfiles/invetory_test /etc/nginx/sites-available/invetory_test

Now we can habilitar the file binding it to site-enable directory
```
sudo ln -s /etc/nginx/sites-available/invetory_test /etc/nginx/sites-enabled
```

Test the config:
```
sudo nginx -t
```

Finnaly we open our firewall to the normal traffict of 80 port:
```
sudo ufw delete allow 8000
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

## Usful commands


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

Creating an admin user

```
docker-compose run web /usr/local/bin/python manage.py createsuperuser
```
