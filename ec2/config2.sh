sudo apt update
sudo apt install docker.io
sudo docker pull ozieblomichal/fastapi-template:dev
docker run -d -p 80:80 fastapi-image
sudo ufw allow 80/tcp
