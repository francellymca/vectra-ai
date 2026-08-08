# Vectra AI

> Enterprise Retrieval-Augmented Generation (RAG) Assistant for Logistics Knowledge Management

---

# Executive Summary

Vectra AI is an enterprise Retrieval-Augmented Generation (RAG) assistant designed to answer logistics-related questions using a curated corporate knowledge base.

Instead of relying solely on a Large Language Model, the assistant retrieves semantically relevant information from indexed corporate documentation before generating responses. This approach reduces hallucinations while providing contextual, traceable and grounded answers.

The project combines workflow automation, vector search, cloud infrastructure and modern AI models to simulate a real-world enterprise knowledge assistant.

---

# Current Status

| Property | Value |
|----------|-------|
| Status | 🟢 Active Development |
| Current Version | **v0.7.0** |
| Architecture | Enterprise Retrieval-Augmented Generation |
| Development Stage | Cloud-Deployed RAG Solution |
| Cloud Deployment | ✅ Oracle Cloud Infrastructure |
| Public Access | ✅ Cloudflare Tunnel (HTTPS) |

## Development Progress

| Component | Status |
|-----------|:------:|
| Docker Environment | ✅ Completed |
| Corporate Knowledge Base | ✅ Completed |
| Automated PDF Generator | ✅ Completed |
| Qdrant Vector Database | ✅ Completed |
| Knowledge Base Ingestion Workflow | ✅ Completed |
| Google Gemini Embeddings | ✅ Completed |
| Groq LLM Integration | ✅ Completed |
| RAG Query Engine | ✅ Completed |
| Vectra AI Assistant | ✅ Completed |
| Oracle Cloud Deployment | ✅ Completed |
| Cloudflare Tunnel | ✅ Completed |
| Telegram Integration | 🚧 In Progress |

---

# Why Vectra AI?

Corporate knowledge is frequently distributed across multiple documents, making information retrieval inefficient, inconsistent and difficult to maintain.

Vectra AI addresses this challenge by combining semantic search, Retrieval-Augmented Generation (RAG), workflow automation and vector databases to provide accurate, grounded and traceable answers based exclusively on corporate documentation.

---

# Solution Overview

The solution is organized into four independent layers.

```text
Corporate Knowledge
        │
        ▼
Knowledge Processing
        │
        ▼
AI Orchestration
        │
        ▼
Grounded Response Generation
```

This layered architecture separates knowledge ingestion from user interaction, allowing the documentation to evolve independently from the conversational assistant.

---

# Production Architecture

```text
                    User
                      │
                      ▼
             Cloudflare Tunnel
                 (HTTPS)
                      │
                      ▼
        Oracle Cloud Infrastructure
                      │
                      ▼
                     n8n
            ┌─────────┼─────────┐
            │         │         │
            ▼         ▼         ▼
        Qdrant      Groq     Gemini
     Vector Store    LLM    Embeddings
            │
            ▼
 Corporate Knowledge Base
```

The production environment runs inside an Oracle Cloud compute instance using Docker containers.

Cloudflare Tunnel provides secure HTTPS access to n8n without requiring direct public exposure of the application port.

---

# RAG Query Flow

The Retrieval-Augmented Generation workflow performs the following steps:

1. The user submits a question.
2. The AI Agent determines whether the corporate knowledge base should be queried.
3. Google Gemini generates the semantic embedding for the question.
4. Qdrant retrieves the most relevant document chunks.
5. Groq generates a grounded response using the retrieved context.
6. The assistant returns the answer together with source attribution whenever available.

---

# Technology Stack

| Layer | Technology |
|------|------------|
| Programming Language | Python |
| Workflow Automation | n8n |
| Vector Database | Qdrant |
| Embeddings | Google Gemini |
| Large Language Model | Groq |
| Containerization | Docker |
| Cloud Infrastructure | Oracle Cloud Infrastructure |
| Secure Public Access | Cloudflare Tunnel |
| Documentation | Markdown + Python |

---

# Repository Structure

```text
vectra-ai/

├── assets/
├── deployment/
│   ├── docker/
│   └── oci/
├── diagrams/
├── docs/
├── screenshots/
├── scripts/
├── tests/
├── workflows/
│   ├── 01 - Knowledge Base Ingestion.json
│   └── 02 - RAG Query Engine.json
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── railway.json
├── README.md
└── requirements.txt
```

---

# Engineering Decisions

## Markdown as the Single Source of Truth

Corporate documentation is maintained in Markdown.

PDF files are automatically generated from Markdown, ensuring consistency while simplifying future maintenance.

---

## Separation of Responsibilities

Knowledge ingestion and question answering are implemented as independent workflows.

This separation allows the knowledge base to be updated without affecting runtime query execution.

---

## Dedicated AI Models

Google Gemini is used for semantic embedding generation.

Groq is used for response generation.

This separation allows each model to perform the task for which it is best suited.

---

## Containerized Environments

Development and production environments are containerized with Docker.

The local environment uses the root Docker Compose configuration, while production uses dedicated deployment files under:

```text
deployment/docker/
```

This separation allows production-specific configuration without affecting local development.

---

## Secure Production Access

The production deployment uses Cloudflare Tunnel to provide HTTPS access to n8n.

This avoids direct public exposure of the n8n application port and provides a secure endpoint for external integrations.

---

# Core Components

| Component | Description |
|----------|-------------|
| Corporate Knowledge Base | Business documentation maintained in Markdown |
| Documentation Builder | Automatic PDF generation pipeline |
| Knowledge Base Ingestion | Reads and indexes corporate documents |
| Vector Database | Semantic search using Qdrant |
| Vectra AI Assistant | Enterprise conversational assistant |
| Retrieval Engine | Retrieves relevant knowledge from the vector database |
| Response Generator | Generates grounded responses using Groq |

---

# Implemented Workflows

| Workflow | Purpose | Status |
|----------|---------|:------:|
| 01 - Knowledge Base Ingestion | Reads corporate PDFs, generates embeddings and stores vectors in Qdrant | ✅ |
| 02 - RAG Query Engine | Retrieves corporate knowledge and generates grounded responses | ✅ |
| 03 - Telegram Assistant | External conversational interface | 🚧 |

---

# Knowledge Base Ingestion

The ingestion workflow performs:

- Reading PDF documents
- Extracting document content
- Splitting text into chunks
- Generating embeddings using Google Gemini
- Associating metadata
- Storing vectors in Qdrant

The production validation confirmed:

```text
Qdrant collection: vectra-kb
Points stored: 50
Status: OK
Optimizer status: OK
```

---

# Vectra AI Assistant

The Vectra AI Assistant is the conversational layer of the platform.

It answers questions exclusively using information retrieved from the corporate knowledge base.

The assistant follows five fundamental principles:

- Retrieval before generation
- Grounded responses
- Source attribution whenever available
- Graceful fallback when no relevant information is found
- No external knowledge outside the configured corporate scope

---

# Validation Results

The cloud deployment has been validated through end-to-end tests.

- ✅ Knowledge base ingestion completed successfully
- ✅ 50 document chunks persisted in Qdrant
- ✅ Semantic retrieval operational
- ✅ Gemini embeddings operational
- ✅ Groq response generation operational
- ✅ Source attribution validated
- ✅ Out-of-domain rejection validated
- ✅ HTTPS access through Cloudflare Tunnel

Example in-domain query:

```text
User:
quero saber sobre a politica de extravios
```

The assistant retrieved the appropriate corporate documentation and returned a grounded response with source attribution.

Example out-of-domain query:

```text
User:
quem ganhou a copa do mundo?
```

The assistant correctly declined to answer because the requested information was not present in the corporate knowledge base.

---

# Production Deployment

Vectra AI has been successfully deployed on Oracle Cloud Infrastructure.

The production environment includes:

- Oracle Cloud Compute Instance
- Ubuntu Server
- Docker Engine
- Docker Compose
- n8n
- Qdrant
- Google Gemini Embeddings
- Groq LLM
- Cloudflare Tunnel

Detailed deployment documentation is available in:

```text
deployment/
├── README.md
└── oci/
    └── README.md
```

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/francellymca/vectra-ai.git
cd vectra-ai
```

Start the Docker environment:

```bash
docker compose up -d
```

Open n8n:

```text
http://localhost:5678
```

Then execute:

1. `01 - Knowledge Base Ingestion`
2. `02 - RAG Query Engine`

---

# Environment Configuration

Development and production configurations are separated.

```text
.env
```

is used for local development.

Production configuration is maintained separately under:

```text
deployment/docker/.env.production
```

Sensitive environment files are not intended to be committed to the repository.

Templates are provided through:

```text
.env.example
deployment/docker/.env.production.example
```

---

# Architecture Documentation

The repository includes documentation covering:

- Solution Architecture
- Knowledge Ingestion Pipeline
- RAG Query Flow
- Local Development Architecture
- Oracle Cloud Deployment Architecture
- Runtime Sequence Diagram

For deployment-specific documentation, see:

```text
deployment/
```

---

# Roadmap

- [x] Project structure
- [x] Docker environment
- [x] Corporate knowledge base
- [x] Automated PDF generation
- [x] Qdrant integration
- [x] Knowledge ingestion workflow
- [x] Google Gemini embeddings
- [x] Groq integration
- [x] Retrieval-Augmented Generation
- [x] Vectra AI Assistant
- [x] Oracle Cloud deployment
- [x] Cloudflare Tunnel
- [ ] Telegram integration
- [ ] Final screenshots and demonstration
- [ ] Final production documentation

---

# Project Scope

Vectra AI is an educational and portfolio project focused on enterprise Retrieval-Augmented Generation (RAG), workflow automation, cloud infrastructure and modern AI engineering practices.

The project emphasizes modular architecture, maintainability, reproducibility, observability and practical integration patterns commonly adopted in enterprise AI systems.