# Oracle Cloud Infrastructure Deployment

This document describes the deployment of Vectra AI on Oracle Cloud Infrastructure (OCI).

The production environment hosts the n8n orchestration layer and the Qdrant vector database inside Docker containers running on an Ubuntu compute instance.

The deployment has been validated with the complete Retrieval-Augmented Generation (RAG) pipeline.

---

## Deployment Status

| Component | Status |
|-----------|:------:|
| OCI Compute Instance | ✅ Completed |
| Ubuntu Server | ✅ Completed |
| SSH Access | ✅ Completed |
| Docker Engine | ✅ Completed |
| Docker Compose | ✅ Completed |
| Repository Deployment | ✅ Completed |
| Production Environment Variables | ✅ Completed |
| n8n Container | ✅ Running |
| Qdrant Container | ✅ Running |
| Knowledge Base Ingestion | ✅ Validated |
| RAG Query Engine | ✅ Validated |
| Cloudflare HTTPS Tunnel | ✅ Validated |
| Telegram Integration | 🚧 In Progress |
| Deployment Evidence | 🚧 In Progress |

---

# Production Architecture

```text
                    Internet
                       │
                       ▼
              Cloudflare Tunnel
                   HTTPS
                       │
                       ▼
             OCI Compute Instance
                       │
                       ▼
                localhost:5678
                       │
                       ▼
                      n8n
                Docker Container
                 │           │
                 │           │
                 ▼           ▼
              Qdrant       External AI APIs
            Vector DB      ├── Gemini Embeddings
                           └── Groq LLM
```

The application runs on an Oracle Cloud compute instance using Docker Compose.

Cloudflare Tunnel provides HTTPS access to the n8n interface without requiring direct exposure of the n8n application port to the public Internet.

Qdrant remains isolated inside the Docker network and is accessed internally by n8n.

---

# OCI Compute Instance

The current deployment uses an Oracle Cloud compute instance with:

| Property | Configuration |
|----------|---------------|
| Operating System | Ubuntu 24.04 LTS |
| Architecture | x86_64 |
| Shape | VM.Standard.E5.Flex |
| OCPUs | 1 |
| Memory | 8 GB |
| Public Network | Enabled |
| Private Subnet Addressing | Enabled |
| SSH Authentication | Public Key |

The application containers run directly on this instance using Docker Compose.

---

# Network Architecture

The OCI environment includes:

- Virtual Cloud Network (VCN)
- Public subnet
- Private subnet
- Internet Gateway
- Route Table
- Security List
- Public IPv4 address
- Primary VNIC

The compute instance is attached to the public subnet.

The route table includes Internet access through the OCI Internet Gateway.

---

# HTTP Connectivity Investigation

During deployment, direct inbound HTTP access through TCP port 80 resulted in connection timeouts even after validating the major network and operating system components.

The following components were verified:

- Public subnet
- Internet Gateway
- Route Table
- Security List
- Public IPv4 assignment
- Primary VNIC
- Ubuntu network interface
- Nginx listening on `0.0.0.0:80`
- Local HTTP connectivity
- Host firewall rules

Local tests confirmed that Nginx responded correctly through both:

```text
http://localhost
```

and:

```text
http://<private-ip>
```

Since the application itself and the OCI network configuration were validated, the deployment strategy was changed to use Cloudflare Tunnel for secure external access.

This avoids exposing the n8n application port directly and provides an HTTPS endpoint suitable for external integrations.

---

# Docker Deployment

The production environment is defined in:

```text
deployment/docker/docker-compose.production.yml
```

Production environment variables are stored separately in:

```text
deployment/docker/.env.production
```

The production environment file is not intended to be committed to source control.

A template is provided through:

```text
deployment/docker/.env.production.example
```

---

# Running the Production Stack

From the project root:

```bash
docker compose \
  --env-file deployment/docker/.env.production \
  -f deployment/docker/docker-compose.production.yml \
  up -d
```

Verify the containers:

```bash
docker ps
```

Expected services:

```text
vectra-n8n
vectra-qdrant
```

---

# Container Architecture

The production stack contains two primary containers.

## n8n

Responsible for:

- Workflow orchestration
- Knowledge ingestion
- RAG execution
- AI Agent execution
- External integrations

The n8n service listens internally on:

```text
5678
```

---

## Qdrant

Responsible for:

- Vector persistence
- Semantic search
- Retrieval of relevant knowledge chunks

Qdrant is not exposed directly to the public Internet.

The n8n container communicates with Qdrant through the Docker network using:

```text
http://vectra-qdrant:6333
```

---

# Docker Network

Both containers are connected to the same private Docker bridge network.

```text
vectra-ai_vectra-network
```

This allows service-to-service communication using container names.

Example:

```text
n8n
 │
 │ http://vectra-qdrant:6333
 ▼
Qdrant
```

This architecture avoids exposing the Qdrant API outside the container network.

---

# Persistent Storage

Docker volumes are used to persist application data.

```text
vectra-ai_n8n_data
vectra-ai_qdrant_storage
```

These volumes preserve:

- n8n configuration
- n8n workflows created in the production instance
- encrypted credentials
- Qdrant collections
- vector data

Container recreation therefore does not remove persistent application data.

---

# Production Environment Variables

The production environment uses a dedicated configuration file.

Important variables include:

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

The production deployment currently uses:

```text
N8N_PORT=5678
N8N_PROTOCOL=https
```

The public host values correspond to the active Cloudflare Tunnel endpoint.

> The active Quick Tunnel URL is temporary and should not be committed to the repository.

---

# Security

The production deployment follows several security principles.

## n8n Encryption Key

The n8n encryption key is maintained only in the production environment file.

It must remain unchanged after credentials have been created because n8n uses it to encrypt stored credentials.

---

## Secrets

The following values must never be committed:

- Gemini API keys
- Groq API keys
- Telegram bot tokens
- n8n encryption keys
- authentication passwords
- SSH private keys

---

## Qdrant Isolation

Qdrant is not mapped to a public host port in the production Docker configuration.

Only services inside the Docker network can access it.

---

## SSH

Administrative access to the OCI instance uses SSH public-key authentication.

Private SSH keys must remain outside the repository.

---

# Cloudflare Tunnel

Cloudflare Tunnel was introduced to provide secure external HTTPS connectivity to n8n.

The current validation environment uses a Cloudflare Quick Tunnel.

Example command:

```bash
cloudflared tunnel --url http://localhost:5678
```

The tunnel creates a temporary HTTPS endpoint similar to:

```text
https://<generated-name>.trycloudflare.com
```

Cloudflare establishes the tunnel through an outbound connection from the OCI instance.

Therefore, the n8n application port does not need to be directly exposed to the public Internet.

---

## Quick Tunnel Limitation

The current deployment uses a Quick Tunnel for development and demonstration purposes.

The generated hostname changes whenever the tunnel is recreated.

Because of this, the following production variables must be updated when the Quick Tunnel URL changes:

```text
N8N_HOST
WEBHOOK_URL
N8N_EDITOR_BASE_URL
```

A future production evolution may use a permanent Cloudflare Tunnel with a custom domain.

---

# Knowledge Base Deployment

Corporate knowledge PDFs are available inside the n8n container through the configured Docker volume.

The Knowledge Base Ingestion workflow reads the files and processes them using:

```text
PDF
 │
 ▼
Document Loader
 │
 ▼
Text Chunks
 │
 ▼
Google Gemini Embeddings
 │
 ▼
Qdrant
```

The production ingestion workflow has been validated successfully.

---

# Qdrant Validation

The production collection is:

```text
vectra-kb
```

Validation results:

```text
status: ok
optimizer_status: ok
points_count: 50
```

The collection contains 50 vector points generated from the corporate knowledge base.

Because Qdrant is isolated inside the Docker network, validation can be performed from the n8n container.

Example:

```bash
docker exec vectra-n8n node -e \
"fetch('http://vectra-qdrant:6333/collections/vectra-kb')
.then(r => r.json())
.then(j => console.log(JSON.stringify(j, null, 2)))
.catch(console.error)"
```

---

# RAG Validation

The production RAG pipeline has been validated end to end.

Validated components:

- Google Gemini embeddings
- Qdrant semantic retrieval
- Groq response generation
- AI Agent orchestration
- Corporate source attribution
- Out-of-domain rejection

Example in-domain request:

```text
quero saber sobre a politica de extravios
```

The assistant successfully retrieved information from the corporate knowledge base and returned a grounded response with source attribution.

Example out-of-domain request:

```text
quem ganhou a copa do mundo?
```

The assistant correctly declined to answer because the requested information was not present in the corporate knowledge base.

This behavior confirms that the assistant follows the configured grounding policy.

---

# Deployment Validation

The following deployment tests have been completed successfully:

- [x] OCI compute instance running
- [x] SSH access
- [x] Docker installation
- [x] Docker Compose installation
- [x] Repository cloned
- [x] Production environment configured
- [x] n8n container running
- [x] Qdrant container running
- [x] Corporate PDFs accessible inside n8n
- [x] Gemini credentials configured
- [x] Groq credentials configured
- [x] Qdrant connection validated
- [x] Knowledge ingestion completed
- [x] 50 vector points persisted
- [x] RAG query validated
- [x] Source attribution validated
- [x] Out-of-domain fallback validated
- [x] HTTPS access through Cloudflare Tunnel
- [ ] Telegram webhook integration
- [ ] Final deployment screenshots

---

# Operational Commands

Check running containers:

```bash
docker ps
```

Check n8n locally:

```bash
curl -I http://localhost:5678
```

Check container logs:

```bash
docker logs vectra-n8n
```

```bash
docker logs vectra-qdrant
```

Restart the production stack:

```bash
docker compose \
  --env-file deployment/docker/.env.production \
  -f deployment/docker/docker-compose.production.yml \
  up -d
```

Stop the production stack:

```bash
docker compose \
  --env-file deployment/docker/.env.production \
  -f deployment/docker/docker-compose.production.yml \
  down
```

---

# Current Deployment Status

The core Vectra AI infrastructure is operational on Oracle Cloud Infrastructure.

Currently validated:

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
 │
 └── Cloudflare Tunnel (HTTPS)
```

The remaining deployment task is the integration of the external Telegram conversational interface.

---

# Next Steps

- [ ] Implement `03 - Telegram Assistant`
- [ ] Configure Telegram credentials
- [ ] Configure Telegram webhook
- [ ] Validate Telegram → RAG → Telegram flow
- [ ] Export the final workflow
- [ ] Capture deployment screenshots
- [ ] Update final project documentation