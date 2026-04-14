# Kiosk AI Implementation Guide

## 1) Configure environment variables in n8n

Use these exact names and dummy defaults first:

- `META_WA_TOKEN="wa_token_dummy_123"`
- `META_WA_PHONE_ID="wa_phone_id_dummy_456"`
- `CLAUDE_API_KEY="sk-ant-dummy-789"`
- `SELCOM_API_KEY="selcom_key_dummy_000"`
- `SELCOM_API_SECRET="selcom_secret_dummy_111"`
- `YANGO_API_KEY="yango_key_dummy_222"`

Add:

- `SELCOM_VENDOR_ID`
- `SELCOM_WEBHOOK_URL`
- `GSHEET_CONFIG_ID`

## 2) Meta WhatsApp setup

1. Create app in Meta for Developers.
2. Add WhatsApp product and connect your business number.
3. Set webhook URL to: `https://<your-n8n-domain>/webhook/wa-inbound`
4. Subscribe to `messages` webhook field.
5. Use permanent system token for production.

## 3) Google Sheets setup

Create one spreadsheet with tabs and columns exactly:

- `Config`: `Shop_Name, AI_Personality_Prompt, Working_Hours, Base_Delivery_Fee`
- `Catalog`: `Item_ID, Item_Name, Price, Stock_Count, Category`
- `Custom_Fleet`: `Rider_Name, Phone_Number, Vehicle_Type, Status`
- `Orders`: `Order_ID, Customer_Phone, Items, Total_Amount, Payment_Status, Dispatch_Status, Rider_Assigned`

Connect Google Sheets OAuth credential in n8n.

## 4) Selcom setup

1. Register callback URL in Selcom:
   `https://<your-n8n-domain>/webhook/selcom-callback`
2. Ensure webhook can reach your n8n instance publicly.
3. Test sandbox push and verify order status update in `Orders`.

## 5) Yango fallback setup

1. Add Yango API base URL and key.
2. Ensure fallback node runs when no rider claim after 60 seconds.
3. Store Yango tracking ID back to `Orders` for customer updates.

## 6) Import workflow and code

1. Import `workflows/kiosk-ai-v1.n8n.json`.
2. Paste scripts from:
   - `n8n-code/parse_whatsapp_flow.py`
   - `n8n-code/selcom_signature.py`
   - `n8n-code/first_rider_wins.py`
3. Set Claude system prompt from `prompts/claude_system_prompt.txt`.

## 7) Production checks

- Keep webhook handlers stateless.
- Use `Order_ID` as correlation key in every branch.
- Add retries and alerting on HTTP failures.
- Log all payment and dispatch transitions.
