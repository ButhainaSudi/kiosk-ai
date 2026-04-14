# Run Local and Ship to Prod

## Local (fast start)

1. Copy env file:
   - `cp .env.example .env`
2. Edit `.env` and set:
   - `WEBHOOK_URL` to your ngrok/cloudflared URL
   - real keys/IDs where available
3. Start services:
   - `docker compose up -d`
4. Open n8n:
   - `http://localhost:5678`
5. Import workflow:
   - `workflows/kiosk-ai-v1.full.n8n.json`
6. Configure Google Sheets credential in n8n UI.
7. Set Meta webhook to:
   - `https://<public-url>/webhook/wa-inbound`
8. Set Selcom callback to:
   - `https://<public-url>/webhook/selcom-callback`

## Local test sequence

1. Send a normal WhatsApp text -> expect Chat route.
2. Submit WhatsApp Flow -> expect order append + Selcom initiation.
3. POST Selcom callback payload manually -> expect paid update + rider broadcast.
4. Click rider button quickly from two rider numbers -> first wins.
5. No rider accept for 60s -> expect Yango fallback call.

## Production deployment

Use the bundled production stack and runbook:

- `docker-compose.prod.yml` — Postgres, n8n (internal), nginx with TLS
- `nginx/` — reverse proxy config (edit `server_name`, add certs under `certs/`)
- `./deploy.sh` — `up`, `down`, `logs`, `backup-db`

Full steps: see `docs/PRODUCTION_DEPLOY.md`.

Summary:

1. Deploy on a VPS/cloud VM with Docker.
2. Copy `.env.example` → `.env`, set `N8N_HOST`, `WEBHOOK_URL`, `N8N_PROTOCOL=https`, `N8N_SECURE_COOKIE=true`.
3. Place `fullchain.pem` and `privkey.pem` in `certs/` (see `certs/README.md`).
4. Run `./deploy.sh up`.
5. Point Meta + Selcom webhooks to `https://<your-domain>/webhook/...`.
6. Enable n8n Error Trigger alerting and schedule `./deploy.sh backup-db`.

## Useful commands

- Start: `docker compose up -d`
- Logs: `docker compose logs -f n8n`
- Stop: `docker compose down`
- Restart n8n only: `docker compose restart n8n`
