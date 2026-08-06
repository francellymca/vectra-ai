# Vectra AI

> Enterprise Retrieval-Augmented Generation (RAG) Assistant for Logistics Knowledge Management

![Status](https://img.shields.io/badge/status-in%20development-green)
![Version](https://img.shields.io/badge/version-v0.3.0-blue)
![Python](https://img.shields.io/badge/python-3.12-blue)
![Docker](https://img.shields.io/badge/docker-ready-2496ED)
![n8n](https://img.shields.io/badge/n8n-workflows-EA4B71)
![Qdrant](https://img.shields.io/badge/Qdrant-vector%20database-red)
![Groq](https://img.shields.io/badge/Groq-LLM-black)
![Gemini](https://img.shields.io/badge/Google-Gemini-blue)

---

# Executive Summary

Vectra AI is an enterprise-oriented Retrieval-Augmented Generation (RAG) assistant designed to answer logistics-related questions using a curated corporate knowledge base.

Instead of relying exclusively on Large Language Models, the solution retrieves semantically relevant information from indexed corporate documents before generating responses. This approach significantly reduces hallucinations while providing contextual, traceable and reliable answers.

The project combines workflow automation, vector databases and modern LLMs to simulate a real-world enterprise knowledge assistant.

---

## Current Status

**Current Version:** v0.4.0

| Component | Status |
|---|---|
| Docker Environment | ✅ Completed |
| Corporate Knowledge Base | ✅ Completed |
| Automated PDF Generator | ✅ Completed |
| Qdrant Vector Database | ✅ Completed |
| Knowledge Base Ingestion Workflow | ✅ Completed |
| Gemini Embeddings | ✅ Completed |
| RAG Query Workflow | ✅ Completed |
| Vectra AI Assistant | ✅ Completed |
| Response Validation and Refinement | 🚧 In Progress |
| Telegram Integration | ⏳ Planned |
| Oracle Cloud Deployment | ⏳ Planned |

---

# Project Objectives

The primary objective of Vectra AI is to demonstrate the implementation of an end-to-end enterprise AI solution capable of:

- Managing a structured corporate knowledge base.
- Performing semantic search using vector embeddings.
- Generating contextual responses using Large Language Models.
- Reducing hallucinations through Retrieval-Augmented Generation.
- Providing a scalable architecture suitable for enterprise environments.

The project also serves as a software engineering portfolio demonstrating practical applications of AI Engineering, workflow automation and cloud-native architecture.

---

# Solution Architecture

![Solution Architecture](diagrams/exports/png/01-solution-architecture.png)

The complete solution is composed of four major layers:

- Knowledge Base
- Vector Storage
- AI Orchestration
- Response Generation

The assistant retrieves relevant document chunks from Qdrant before sending contextual information to the LLM, ensuring grounded responses.

## RAG Query Workflow

![RAG Query Flow](diagrams/exports/png/02-rag-query-flow.png)

The query workflow follows this sequence:

1. The user sends a question through the n8n chat interface.
2. The AI Agent determines whether the corporate knowledge base must be queried.
3. Google Gemini generates the semantic embedding for the question.
4. Qdrant retrieves the most relevant document chunks.
5. Groq generates the final answer using the retrieved context.
6. The assistant returns a grounded response and identifies the source document when available.

---

# Technology Stack

| Layer | Technology |
|--------|------------|
| Programming Language | Python |
| Workflow Automation | n8n |
| Vector Database | Qdrant |
| Embeddings | Google Gemini |
| Large Language Model | Groq |
| Containerization | Docker |
| Documentation | Markdown + Python |
| Deployment | Oracle Cloud Infrastructure (planned) |

---

# Repository Structure

```text
vectra-ai/

assets/
deployment/
diagrams/
docs/
screenshots/
scripts/
tests/
workflows/

docker-compose.yml
README.md
requirements.txt
```

---

# Engineering Decisions

Several architectural decisions were intentionally made during development to improve maintainability, scalability and reproducibility.

### Markdown as the single source of truth

All knowledge documents are authored in Markdown.

PDF documents are automatically generated from Markdown, ensuring documentation consistency while simplifying future updates.

---

### Workflow separation

Knowledge ingestion and question answering are implemented as independent workflows.

This separation allows the knowledge base to be rebuilt without affecting runtime query execution.

---

### Dedicated embedding model

Google Gemini is used exclusively for embedding generation.

Groq is reserved for response generation, taking advantage of its inference speed while maintaining compatibility with vector search requirements.

---

### Containerized development

The entire development environment runs inside Docker Compose.

This guarantees reproducibility across different machines and simplifies deployment to cloud environments.

---

## Implemented Workflows

| Workflow | Status | Description |
|---|---|---|
| 01 - Knowledge Base Ingestion | ✅ Completed | Reads corporate PDF documents, splits the content into chunks, generates embeddings with Google Gemini and stores the vectors in Qdrant. |
| 02 - RAG Query Engine | ✅ Completed | Receives user questions, retrieves relevant corporate information from Qdrant and generates grounded responses using Groq. |
| 03 - Telegram Assistant | ⏳ | Conversational interface |
| 04 - OCI Deployment | ⏳ | Cloud deployment |

---

# Knowledge Ingestion Pipeline

![Knowledge Ingestion](diagrams/exports/png/03-knowledge-ingestion.png)

The ingestion workflow currently performs:

1. Reads PDF documents
2. Extracts document content
3. Splits text into semantic chunks
4. Generates vector embeddings
5. Associates metadata
6. Stores vectors inside Qdrant

---

## Vectra AI Assistant

The **Vectra AI Assistant** is the conversational layer of the project.

It receives questions in Brazilian Portuguese, searches the corporate knowledge base and generates answers based exclusively on the retrieved documentation.

The assistant currently supports:

- shipping policies;
- order tracking;
- refunds and claims;
- customer service and complaints;
- frequently asked questions;
- operational procedures.

When no relevant information is found, the assistant does not use external knowledge and informs the user that the requested topic is not available in the documentation.

---

# Running Locally

Clone the repository

```bash
git clone https://github.com/francellymca/vectra-ai.git
```

Start Docker services

```bash
docker compose up -d
```

Open n8n

```
http://localhost:5678
```

Execute the Knowledge Base Ingestion workflow.

---

# Example Questions

The assistant is expected to answer questions such as:

- Como funciona a política de reembolsos?

---

# Example Response

The assistant retrieves the corporate refund and claims documentation and returns information about:

- the purpose and scope of the policy;
- the estimated analysis period;
- possible outcomes of the request;
- the corresponding source document.

### Out-of-Scope Question

> Me fale sobre a Copa do Mundo.

### Expected Behavior

The assistant informs the user that no corresponding information was found in the corporate knowledge base and does not generate an answer using external knowledge.

Source:
refund-policy.pdf

Section:
Refund Procedures

Confidence:
0.94
```

---

# Architecture Documentation

The repository includes complete architectural documentation.

| Diagram | Description |
|----------|-------------|
| Solution Architecture | Overall system architecture |
| RAG Query Flow | End-to-end retrieval process |
| Knowledge Ingestion | Vector indexing pipeline |
| Local Development | Docker-based architecture |
| OCI Deployment | Cloud deployment architecture |
| Sequence Diagram | Runtime interaction between components |

---

## Roadmap

- [x] Project structure
- [x] Docker environment
- [x] Corporate knowledge base
- [x] Automated PDF generation
- [x] Qdrant integration
- [x] Knowledge ingestion workflow
- [x] Gemini embedding generation
- [x] RAG query workflow
- [x] Vectra AI Assistant
- [ ] Prompt and response refinement
- [ ] Telegram integration
- [ ] OCI deployment
- [ ] Final documentation and evidence

---

# Project Scope

Vectra AI is an educational and portfolio project focused on exploring enterprise Retrieval-Augmented Generation (RAG), workflow automation and cloud-native AI architectures.

Rather than providing a production-ready application, the project emphasizes software engineering practices, system architecture, maintainability and AI integration strategies commonly found in enterprise environments.