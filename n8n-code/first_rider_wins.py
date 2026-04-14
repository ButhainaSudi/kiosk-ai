import re
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
    rider_phone = msg.get("from", "")
    button_id = safe_get(msg, ["interactive", "button_reply", "id"], "")

    m = re.match(r"^ACCEPT_ORD_(.+)$", button_id)
    if not m:
        out.append({"json": {"ok": False, "reason": "invalid_button_id"}})
        continue

    order_id = m.group(1)
    order_row = root.get("order_row", {})
    current_rider = (order_row.get("Rider_Assigned") or "").strip()

    if current_rider:
        out.append({
            "json": {
                "ok": False,
                "order_id": order_id,
                "assigned_to": current_rider,
                "message_to_rider": "Samahani, kazi hii tayari imechukuliwa."
            }
        })
        continue

    out.append({
        "json": {
            "ok": True,
            "order_id": order_id,
            "winner_rider_phone": rider_phone,
            "update_patch": {
                "Rider_Assigned": rider_phone,
                "Dispatch_Status": "ASSIGNED_CUSTOM_FLEET",
                "Assigned_At": datetime.now(timezone.utc).isoformat()
            }
        }
    })

return out
