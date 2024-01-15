sudo apt update
sudo apt install docker.io
sudo docker pull ozieblomichal/fastapi-template:amd
sudo docker run -d -p 8000:8000 f95642a932af
sudo ufw allow 8000/tcp
