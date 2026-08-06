
# Oracle Cloud Infrastructure Deployment

This document describes the deployment of Vectra AI on Oracle Cloud Infrastructure.

## Target Architecture

The application will run on an Ubuntu compute instance using Docker Compose.

The deployment will include:

- n8n;
- Qdrant;
- persistent data volumes;
- public network access;
- HTTPS configuration;
- Telegram webhook support.

## Deployment Steps

- [ ] Create the OCI compute instance
- [ ] Configure networking and security rules
- [ ] Connect to the instance through SSH
- [ ] Install Docker
- [ ] Install Docker Compose
- [ ] Clone the repository
- [ ] Configure environment variables
- [ ] Start the production stack
- [ ] Configure HTTPS
- [ ] Validate n8n and Qdrant
- [ ] Connect the Telegram webhook
- [ ] Capture deployment evidence