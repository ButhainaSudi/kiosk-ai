# TLS certificates for nginx (production)

Place PEM files here so the `nginx` service can mount them:

- `fullchain.pem` — full certificate chain (e.g. Let's Encrypt `fullchain.pem`)
- `privkey.pem` — private key

Example (on the host, after obtaining certs with certbot):

```bash
sudo cp /etc/letsencrypt/live/your.domain/fullchain.pem ./certs/fullchain.pem
sudo cp /etc/letsencrypt/live/your.domain/privkey.pem ./certs/privkey.pem
sudo chown "$USER" ./certs/*.pem
```

For a **temporary self-signed** cert for internal testing only:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout privkey.pem -out fullchain.pem \
  -subj "/CN=n8n.local"
```

Update `nginx/conf.d/n8n.conf` `server_name` to match your domain before going live.
