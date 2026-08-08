# Deployment

<<<<<<< HEAD
This directory contains the infrastructure and deployment resources required to run Vectra AI outside the local development environment.

The current validated production target is **Oracle Cloud Infrastructure (OCI)** using Docker Compose.

Secure external access to the n8n instance is provided through **Cloudflare Tunnel (HTTPS)**.

---

# Deployment Status

| Component | Status |
|-----------|:------:|
| Oracle Cloud Infrastructure | ✅ Completed |
| Docker Production Stack | ✅ Completed |
| n8n | ✅ Running |
| Qdrant | ✅ Running |
| Production Environment Configuration | ✅ Completed |
| Cloudflare Tunnel | ✅ Completed |
| Knowledge Base Ingestion | ✅ Validated |
| RAG Query Engine | ✅ Validated |
| Telegram Integration | 🚧 In Progress |
| Final Deployment Evidence | 🚧 In Progress |
=======


## Directory Structure

```text
deployment/
├── docker/
│   ├── docker-compose.production.yml
│   ├── .env.production.example
<<<<<<< HEAD
│   └── .env.production
│
├── oci/
│   └── README.md
│
└── README.md
=======
│   └── README.md



> `.env.production` contains environment-specific and sensitive configuration and must not be committed to source control.

---

<<<<<<< HEAD
# Deployment Architecture

```text
                    Internet
                       │
                       ▼
              Cloudflare Tunnel
                   HTTPS
                       │
                       ▼
        Oracle Cloud Infrastructure
                       │
                       ▼
              Docker Compose
                 │         │
                 ▼         ▼
               n8n       Qdrant
                 │
                 ├── Google Gemini Embeddings
                 └── Groq LLM
```

The production environment separates public access from internal service communication.

n8n is exposed through Cloudflare Tunnel, while Qdrant remains isolated inside the Docker network.
=======
### Cloudflared

Contains the Cloudflare Tunnel configuration used to securely expose the n8n instance without opening inbound ports.

<<<<<<< HEAD
- Oracle Cloud Compute Instance
- Ubuntu Server
- Docker Engine
- Docker Compose
- n8n workflow automation
- Qdrant vector database
- Persistent Docker volumes
- Google Gemini embeddings
- Groq LLM
- Cloudflare Tunnel for HTTPS access
- Telegram integration (in progress)

---

# Production Configuration

Production configuration is maintained separately from the local development environment.

The production Docker stack is defined in:

```text
deployment/docker/docker-compose.production.yml
```

Environment-specific values are stored in:

```text
deployment/docker/.env.production
```

A safe configuration template is provided through:

```text
deployment/docker/.env.production.example
```

---

# Environment Preparation

Create the production environment file from the provided template:

```bash
cp deployment/docker/.env.production.example \
   deployment/docker/.env.production
```

Then edit:

```text
deployment/docker/.env.production
```

with the appropriate production values.

Typical configuration includes:

```text
N8N_HOST
N8N_PORT
N8N_PROTOCOL
WEBHOOK_URL
N8N_EDITOR_BASE_URL
GENERIC_TIMEZONE
TZ
N8N_ENCRYPTION_KEY
N8N_SECURE_COOKIE
```

Sensitive values must never be committed to the repository.

---

# Starting the Production Stack

From the repository root:

```bash
docker compose \
  --env-file deployment/docker/.env.production \
  -f deployment/docker/docker-compose.production.yml \
  up -d
```

Verify the running containers:

```bash
docker ps
```

Expected services:

```text
vectra-n8n
vectra-qdrant
```

---

# Production Networking

The production stack uses a private Docker bridge network for communication between services.

n8n connects to Qdrant internally using:

```text
http://vectra-qdrant:6333
```

Qdrant is not directly exposed to the public Internet.

External HTTPS access to n8n is provided through Cloudflare Tunnel.

---

# Persistent Storage

Docker volumes are used to preserve application state.

The production environment maintains persistent storage for:

- n8n configuration
- n8n credentials
- n8n workflow data
- Qdrant collections
- Vector data

Container recreation does not remove persisted application data.

---

# Deployment Validation

The OCI deployment has been validated successfully.

Completed tests include:

- [x] OCI compute instance provisioning
- [x] SSH access
- [x] Docker installation
- [x] Docker Compose installation
- [x] Repository deployment
- [x] Production environment configuration
- [x] n8n container startup
- [x] Qdrant container startup
- [x] Corporate PDF availability
- [x] Gemini embeddings
- [x] Qdrant vector persistence
- [x] 50 vector points stored
- [x] RAG query execution
- [x] Source attribution
- [x] Out-of-domain query rejection
- [x] HTTPS access through Cloudflare Tunnel
- [ ] Telegram webhook integration
- [ ] Final deployment screenshots

---

# Deployment Documentation

Detailed Oracle Cloud deployment documentation is available in:

```text
deployment/oci/README.md
```

That document contains:

- OCI compute configuration
- Network architecture
- Docker installation
- Production stack setup
- Cloudflare Tunnel configuration
- Qdrant validation
- RAG validation
- Troubleshooting notes
- Operational commands

---

# Local vs Production Environments

Vectra AI keeps local and production configuration separated.

```text
Local Development
├── docker-compose.yml
└── .env

Production
├── deployment/docker/docker-compose.production.yml
└── deployment/docker/.env.production
```

This separation allows infrastructure-specific configuration to evolve without affecting the local development environment.

---

# Current Deployment State

The core production environment is operational.

```text
OCI
 │
 ├── Ubuntu
 │
 ├── Docker
 │   ├── n8n
 │   └── Qdrant
 │
 ├── Gemini Embeddings
 ├── Groq LLM
 └── Cloudflare Tunnel
```

The remaining integration task is the external Telegram conversational interface.

---

# Next Steps

- [ ] Implement `03 - Telegram Assistant`
- [ ] Configure Telegram credentials
- [ ] Configure Telegram webhook
- [ ] Validate Telegram → RAG → Telegram flow
- [ ] Export the final workflow
- [ ] Capture final deployment evidence
- [ ] Complete production documentation