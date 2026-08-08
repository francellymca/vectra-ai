sudo apt update
sudo apt install docker.io docker-compose-plugin git -y

sudo mkdir -p /opt/vectra-ai

cd /opt/vectra-ai

git clone ...

docker compose -f deployment/docker/docker-compose.production.yml up -d