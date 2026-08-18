# Cloudflared Tunnel

> **Previous Deployment Architecture**
>
> Cloudflare Tunnel (Cloudflared) was used during the initial production deployment of Vectra AI to securely expose the n8n web interface without directly opening inbound application ports on the Oracle Cloud Infrastructure (OCI) virtual machine.
>
> The current production architecture uses **DuckDNS, Nginx and Let's Encrypt** to provide persistent domain resolution, reverse proxy routing and HTTPS access.
>
> This documentation is retained as part of the project's infrastructure evolution and as a reference for an alternative secure deployment strategy.

---

## Purpose

In the initial deployment architecture, Cloudflared created an encrypted outbound connection from the OCI VM to the Cloudflare network.

This approach allowed the n8n service to be accessed externally without directly exposing its application port to the Internet.

---

## Previous  Architecture

```
Internet
     │
     ▼
Cloudflare Edge
     │
Encrypted Tunnel
     │
Cloudflared Service
     │
OCI Virtual Machine
     │
Docker Network
     │
n8n
```

---

## Configuration

The deployment includes the following files:

```
deployment/
└── cloudflared/
    ├── config.yml
    └── install-cloudflared.sh
```

### config.yml

Responsible for:

- Tunnel configuration
- Public hostname
- Local destination service
- HTTP routing

### install-cloudflared.sh

Automates:

- Cloudflared installation
- Binary download
- Service configuration
- Tunnel startup

---

## Historical Deployment Flow

1. Install Cloudflared
2. Authenticate the tunnel
3. Configure `config.yml`
4. Register as a systemd service
5. Start the tunnel
6. Access n8n securely through Cloudflare

---

## Security

The Cloudflared-based deployment provided the following security characteristics:

- No inbound ports exposed
- Encrypted tunnel
- Zero Trust architecture
- Cloudflare-managed TLS
- Reduced attack surface

---

## Benefits

- Secure remote access
- Easy deployment
- No public reverse proxy required
- Automatic HTTPS
- Compatible with Oracle Cloud Free Tier

---

## Current Production Architecture

The current Vectra AI production environment replaced Cloudflare Tunnel with a persistent domain and reverse proxy architecture based on:

- DuckDNS for domain resolution
- Nginx as the reverse proxy
- Let's Encrypt for TLS certificates and HTTPS
- Oracle Cloud Infrastructure as the compute environment
- Docker for application containerization

The Cloudflared implementation remains documented in this repository to preserve the architectural history of the project and provide an alternative deployment reference.
