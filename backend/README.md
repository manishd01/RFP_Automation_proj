FastAPI backend for AI-Powered RFP system.

Run locally:
    cd backend
    pip install -r requirements.txt
    uvicorn app.main:app --reload --port 8000

With Docker:
    docker-compose up --build

API notes:
- POST /api/rfps/ -> create RFP (will run light-weight AI extraction if OPENAI_API_KEY set)
- POST /api/vendors/ -> create vendor
- POST /api/vendors/send/{vendor_id}/{rfp_id} -> send RFP via SMTP (requires SMTP env configured)
- POST /api/vendors/receive_proposal -> accepts JSON {vendor_id, rfp_id, raw_email} to ingest a proposal (useful for testing or IMAP hook)
- GET /api/proposals/for_rfp/{rfp_id} -> list proposals for a given RFP
