#!/bin/bash

sudo apt update
sudo apt upgrade -y

sudo apt install -y \
    docker.io \
    docker-compose-plugin \
    git \
    curl

sudo systemctl enable docker
sudo systemctl start docker

sudo usermod -aG docker ubuntu