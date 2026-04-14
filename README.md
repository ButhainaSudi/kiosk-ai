# Kiosk AI

WhatsApp automation for SMEs in Tanzania: conversational AI (Claude), deterministic checkout via WhatsApp Flows + Google Sheets, Selcom payments, and bodaboda dispatch (custom fleet first, Yango fallback). Orchestration runs in **n8n**; this repo holds workflow exports, Python snippets for n8n Code nodes, prompts, and Docker-based run instructions.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose v2
- A Google Sheet with the tabs/columns described in `docs/IMPLEMENTATION_GUIDE.md`
- For real webhooks: a **public HTTPS URL** (e.g. ngrok in dev, your domain in prod)

## Quick start (local development)

1. **Environment**

   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set at least:

   - `WEBHOOK_URL` — your public base URL (ngrok/cloudflared in dev), e.g. `https://abc123.ngrok-free.app`
   - `SELCOM_WEBHOOK_URL` — usually `https://<same-host>/webhook/selcom-callback`
   - `GSHEET_CONFIG_ID` — Google Spreadsheet ID
   - API keys and secrets as you obtain them

   For the Claude system prompt, use the text in `prompts/claude_system_prompt.txt` (paste into `.env` as one line or with `\n` escaped).

2. **Start n8n + Postgres**

   ```bash
   docker compose up -d
   ```

3. **Open n8n**

   - UI: [http://localhost:5678](http://localhost:5678)
   - Complete first-time setup if prompted.

4. **Import the workflow**

   - In n8n: **Workflows → Import from File**
   - Choose `workflows/kiosk-ai-v1.full.n8n.json` (full routing) or `workflows/kiosk-ai-v1.n8n.json` (minimal skeleton)

5. **Connect Google Sheets** in the n8n UI (OAuth credentials) and align sheet column names with the workflow.

6. **Expose webhooks**

   Point Meta WhatsApp and Selcom callbacks at your public URL:

   - WhatsApp: `https://<your-public-host>/webhook/wa-inbound`
   - Selcom: `https://<your-public-host>/webhook/selcom-callback`

## Production (nginx + TLS)

Use the production Compose file and helper script:

```bash
cp .env.example .env
# Edit .env: N8N_HOST, N8N_PROTOCOL=https, WEBHOOK_URL, N8N_SECURE_COOKIE=true, strong secrets
# Put TLS certs in certs/ — see certs/README.md
# Edit nginx/conf.d/n8n.conf server_name to match your domain
./deploy.sh up
```

Details: **`docs/PRODUCTION_DEPLOY.md`**.

## Project layout

| Path | Description |
|------|-------------|
| `workflows/` | n8n workflow JSON exports |
| `n8n-code/` | Python scripts to paste into n8n **Code** nodes |
| `prompts/` | Claude system prompt |
| `docs/` | Implementation guide, local/prod run notes |
| `docker-compose.yml` | Local stack (n8n + Postgres, port 5678) |
| `docker-compose.prod.yml` | Prod stack (n8n internal + nginx + Postgres) |
| `deploy.sh` | `./deploy.sh up`, `down`, `logs`, `backup-db`, etc. |

## Useful commands

| Goal | Command |
|------|---------|
| Start local stack | `docker compose up -d` |
| View logs | `docker compose logs -f n8n` |
| Stop local stack | `docker compose down` |
| Start production stack | `./deploy.sh up` |
| Production logs | `./deploy.sh logs` |
| Backup Postgres (prod compose) | `./deploy.sh backup-db` |

## Further reading

- `docs/IMPLEMENTATION_GUIDE.md` — Meta, Sheets, Selcom checklist
- `docs/RUN_LOCAL_AND_PROD.md` — local test sequence and production summary
- `docs/PRODUCTION_DEPLOY.md` — nginx, TLS, operations
