#!/bin/bash

curl -fsSL https://pkg.cloudflare.com/install.sh | sudo bash
sudo apt update
sudo apt install -y cloudflared