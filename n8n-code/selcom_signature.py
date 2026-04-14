import os
import json
import hmac
import hashlib
from datetime import datetime, timezone


def canonical_json(payload: dict) -> str:
    return json.dumps(payload, separators=(",", ":"), sort_keys=True)


out = []
for item in items:
    src = item.get("json", {})

    api_key = os.getenv("SELCOM_API_KEY", "selcom_key_dummy_000")
    api_secret = os.getenv("SELCOM_API_SECRET", "selcom_secret_dummy_111")
    vendor_id = os.getenv("SELCOM_VENDOR_ID", "vendor_dummy_001")
    callback_url = os.getenv("SELCOM_WEBHOOK_URL", "https://n8n.yourdomain.com/webhook/selcom-callback")

    payload = {
        "vendor": vendor_id,
        "order_id": src["order_id"],
        "buyer_email": src.get("buyer_email", "customer@example.com"),
        "buyer_name": src.get("buyer_name", "WhatsApp Customer"),
        "buyer_phone": src["buyer_phone"],
        "amount": float(src["amount"]),
        "currency": src.get("currency", "TZS"),
        "webhook_url": callback_url,
        "payment_methods": ["SELCOM_PAY/MASTERCARD"]
    }

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    body_string = canonical_json(payload)
    signing_string = f"{timestamp}.{body_string}"

    signature = hmac.new(
        api_secret.encode("utf-8"),
        signing_string.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    out.append({
        "json": {
            "payload": payload,
            "headers": {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "X-Timestamp": timestamp,
                "X-Signature": signature,
                "X-Api-Key": api_key
            }
        }
    })

return out
