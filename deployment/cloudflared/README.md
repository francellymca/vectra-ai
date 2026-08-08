# Cloudflared Tunnel

The Vectra AI production environment uses **Cloudflare Tunnel (Cloudflared)** to securely expose the n8n web interface without opening inbound ports on the Oracle Cloud Infrastructure (OCI) virtual machine.

---

## Purpose

Cloudflared creates an encrypted outbound connection from the OCI VM to the Cloudflare network.

This approach eliminates the need to expose ports such as **80**, **443** or **5678** directly to the Internet, providing an additional security layer.

---

## Architecture

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

## Deployment Flow

1. Install Cloudflared
2. Authenticate the tunnel
3. Configure `config.yml`
4. Register as a systemd service
5. Start the tunnel
6. Access n8n securely through Cloudflare

---

## Security

Cloudflared improves the deployment security by:

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