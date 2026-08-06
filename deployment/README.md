# Vectra AI Deployment

This directory contains the infrastructure and deployment resources required to run Vectra AI in a production environment.

The current deployment target is **Oracle Cloud Infrastructure (OCI)** using Docker Compose.

---

# Directory Structure

```text
deployment/
├── docker/
│   ├── docker-compose.production.yml
│   └── .env.production.example
├── oci/
│   └── README.md
└── README.md
```

---

# Deployment Preparation

Before starting the deployment, create the production environment file from the provided template.

```bash
cp .env.production.example .env.production
```

Then edit the `.env.production` file with the production values appropriate for your environment.

---

# Deployment Components

The production environment includes:

- n8n workflow automation
- Qdrant vector database
- Persistent Docker volumes
- HTTPS public access
- Telegram webhook integration

---

# Deployment Status

🚧 In Progress