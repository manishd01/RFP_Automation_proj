# Communication logs
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..deps import get_db
from .. import models, schemas, crud,  compare

router = APIRouter()
# Create communication log entry
@router.post("", response_model=dict)
def create_comm(c: schemas.CommunicationLogCreate , db: Session = Depends(get_db)):
    obj = crud.create_communication(db, c)
    return {"id": obj.id, "status": obj.status}

# List all logs for an RFP
@router.get("/for_rfp/{rfp_id}")
def list_logs_for_rfp(rfp_id: int, db: Session = Depends(get_db)):
    return crud.list_communication_logs_for_rfp(db, rfp_id)

# Mark a log as replied
@router.post("/mark_reply/{log_id}")
def mark_reply(log_id: int, db: Session = Depends(get_db)):
    log = crud.mark_reply_received(db, log_id)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

# Update status
@router.post("/update_status/{log_id}")
def update_status(log_id: int, status: str, db: Session = Depends(get_db)):
    log = crud.update_communication_log_status(db, log_id, status)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

# Comparison
@router.post("/rfps/{rfp_id}/compare")
def run_compare(rfp_id:int, db: Session = Depends(get_db)):
    # returns ranked proposals
    return compare.compare_rfp(db, rfp_id)

@router.post("/rfps/{rfp_id}/select/{proposal_id}")
def select_winner(rfp_id:int, proposal_id:int, db: Session = Depends(get_db)):
    # mark a proposal as selected: here we update a status in communication log or proposal score?
    p = db.query(models.Proposal).filter(models.Proposal.id==proposal_id, models.Proposal.rfp_id==rfp_id).first()
    if not p:
        raise HTTPException(404, "Proposal not found")
    # simple flag: write communication log entry
    from datetime import datetime
    log = models.CommunicationLog(rfp_id=rfp_id, vendor_id=p.vendor_id, proposal_id=p.id, direction="internal", email_type="selection", subject="Selected", raw_email=f"Selected on {datetime.utcnow().isoformat()}", reply_received=False, status="selected")
    db.add(log); db.commit()
    return {"status":"selected", "proposal_id": p.id}