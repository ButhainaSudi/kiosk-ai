import json
from datetime import datetime, timezone


def safe_get(dct, path, default=None):
    cur = dct
    for key in path:
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur


out = []
for item in items:
    root = item.get("json", {})
    msg = safe_get(root, ["entry", 0, "changes", 0, "value", "messages", 0], {})
    customer_phone = msg.get("from", "")
    interactive = msg.get("interactive", {})
    nfm_reply = interactive.get("nfm_reply", {})

    raw_response_json = nfm_reply.get("response_json", "{}")
    if isinstance(raw_response_json, str):
        flow_data = json.loads(raw_response_json)
    else:
        flow_data = raw_response_json or {}

    structured = {
        "source": "whatsapp_flow_submission",
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "customer_phone": customer_phone,
        "buyer_name": flow_data.get("buyer_name", "WhatsApp Customer"),
        "buyer_email": flow_data.get("buyer_email", "customer@example.com"),
        "buyer_phone": flow_data.get("buyer_phone", customer_phone),
        "delivery_address": flow_data.get("delivery_address", ""),
        "cart_items": flow_data.get("cart_items", []),
        "total_amount": flow_data.get("total_amount", 0),
        "flow_token": nfm_reply.get("flow_token", ""),
        "flow_response": flow_data
    }
    out.append({"json": structured})

return out
