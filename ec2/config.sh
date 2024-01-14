#!/bin/bash
apt-get update -y
sudo apt install -y python3 python3-pip apache2 certbot python3-certbot-apache
sudo apt install -y docker.io

sudo docker pull ozieblomichal/fastapi-template:dev

sudo docker build -t fastapi-template .

sudo docker run -d -p 8000:8000 fastapi-template

cd /etc/apache2/sites-available/
vi 000-default-le-ssl.conf
# edit ProxyPass and ProxyPassReverse lines to look like this:
# ProxyPass / http://localhost:8000/
# ProxyPassReverse / http://localhost:8000/

sudo a2enmod proxy
sudo a2enmod proxy_http

udo systemctl restart apache2

sudo certbot --apache -d your_domain.com
