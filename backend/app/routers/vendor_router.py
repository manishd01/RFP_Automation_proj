from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..deps import get_db
from ..services import email_service, ai_service
from ..utils.email_parser import parse_vendor_email
import json
from sqlalchemy.exc import IntegrityError
router = APIRouter()

# @router.post("/", response_model=schemas.VendorResponse)
# async def create_vendor(vendor_in: schemas.VendorCreate, db: Session = Depends(get_db)):
#     new_vendor = crud.create_vendor(db, vendor_in)
#     db.add(new_vendor)
#     try:
#         db.commit()
#         db.refresh(new_vendor)
#         return new_vendor
#     except IntegrityError as e:
#         db.rollback()
#         # Check if it's duplicate email error
#         if "Duplicate entry" in str(e.orig):
#             raise HTTPException(status_code=409, detail=f"Email {vendor_in.email} already exists.")
#         else:
#             raise HTTPException(status_code=400, detail="Database error")

#  //simple   
@router.post("/", response_model=schemas.VendorResponse)
async def create_vendor(vendor_in: schemas.VendorCreate, db: Session = Depends(get_db)):
    v = crud.create_vendor(db, vendor_in)
    return v


@router.get("/", response_model=list[schemas.VendorResponse])
async def list_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_vendors(db, skip=skip, limit=limit)

# RFP #1: Laptop & Monitor Quote subject:
@router.post("/send/{vendor_id}/{rfp_id}")
async def send_rfp_to_vendor(vendor_id: int, rfp_id: int, db: Session = Depends(get_db)):
    vendor = crud.get_vendor(db, vendor_id)
    rfp = crud.get_rfp(db, rfp_id)
    
    if not vendor or not rfp: 
        raise HTTPException(status_code=404, detail="Vendor or RFP not found")

    subject = f"RFP #{rfp.id}: {rfp.title} , vendor id: {vendor.id}"

    # Convert structured RFP to JSON string if it exists
    # if isinstance(rfp.structured, dict):
    #     body_to_send = json.dumps(rfp.structured)
    # else:
    #     body_to_send = rfp.description  # fallback plain text

    body_to_send=rfp.structured
    raw_text_mail= rfp.description
    sent = email_service.send_rfp_email(db, vendor_id, rfp_id ,vendor.email, subject, body_to_send,  raw_text_mail)
    return {"sent": sent}


@router.post('/receive_proposal')
async def receive_proposal(proposal_in: schemas.ProposalIn, db: Session = Depends(get_db)):
    # 1️⃣ Parse raw email
    parsed = parse_vendor_email(proposal_in.raw_email)
    proposal_json = {'text': parsed.get('text'), 'attachments': parsed.get('attachments')}
    print("Parsed proposal:", proposal_json)
    # 2️⃣ Score proposal
    rfp = crud.get_rfp(db, proposal_in.rfp_id)
    structured = rfp.structured if rfp else None
    score_obj = ai_service.score_proposal_against_rfp(structured, proposal_json)

    # 3️⃣ Create proposal
    print("Creating proposal with score:", score_obj)
    created = crud.create_proposal(
        db,
        proposal_in.vendor_id,
        proposal_in.rfp_id,
        proposal_in.raw_email,
        proposal_json,
        score=score_obj.get('score')
    )

    # 4️⃣ Create communication log automatically
    comm_log_in = schemas.CommunicationLogCreate(
        rfp_id=proposal_in.rfp_id,
        vendor_id=proposal_in.vendor_id,
        proposal_id=created.id,
        direction="inbound",
        email_type="proposal",
        subject=parsed.get('subject'),
        raw_email=proposal_in.raw_email,
        status="received",
        attempt_count=1,
        reply_received=True
    )
    crud.create_communication_log(db, comm_log_in)

    # 5️⃣ Return response
    return {'proposal_id': created.id, 'score': score_obj}

