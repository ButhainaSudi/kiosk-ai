# Production deploy (nginx + TLS + Postgres + n8n)

## Files

| File | Purpose |
|------|---------|
| `docker-compose.prod.yml` | Postgres, n8n (internal), nginx (80/443) |
| `nginx/nginx.conf` | Main nginx config |
| `nginx/conf.d/n8n.conf` | Reverse proxy + TLS server blocks |
| `certs/` | Mount `fullchain.pem` and `privkey.pem` here |
| `deploy.sh` | One-command up/down/logs/backup |

## One-time setup

1. Copy environment:
   - `cp .env.example .env`
2. Set production values (minimum):
   - `N8N_HOST` — your public hostname (e.g. `n8n.yourdomain.com`)
   - `N8N_PROTOCOL=https`
   - `WEBHOOK_URL=https://n8n.yourdomain.com`
   - `SELCOM_WEBHOOK_URL=https://n8n.yourdomain.com/webhook/selcom-callback`
   - `N8N_SECURE_COOKIE=true`
   - Strong `N8N_ENCRYPTION_KEY`, `POSTGRES_PASSWORD`, and API keys
3. Edit `nginx/conf.d/n8n.conf` and replace `n8n.yourdomain.com` with your real domain.
4. Put TLS PEMs in `certs/` (see `certs/README.md`).
5. Start:
   - `chmod +x deploy.sh`
   - `./deploy.sh up`

Open `https://your-domain` and complete n8n first-time setup if prompted.

## Meta + Selcom webhooks

Point both to your public HTTPS origin (same host as `WEBHOOK_URL`):

- Meta WhatsApp: `https://your-domain/webhook/wa-inbound`
- Selcom: `https://your-domain/webhook/selcom-callback`

## Operations

- Logs: `./deploy.sh logs`
- Status: `./deploy.sh ps`
- Stop: `./deploy.sh down`
- DB backup: `./deploy.sh backup-db`

## TLS renewal (Let's Encrypt)

Renew certs on the host, then copy PEMs into `certs/` again (or mount `/etc/letsencrypt` read-only) and reload nginx:

```bash
docker compose -f docker-compose.prod.yml exec nginx nginx -s reload
```

## Security notes

- Do not expose Postgres or n8n ports publicly; only nginx publishes 80/443.
- Restrict SSH and firewall to required ports only.
- Rotate keys on a schedule; keep `.env` out of version control.
