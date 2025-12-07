from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from datetime import datetime
from .compare import score_proposal


def create_rfp(db: Session, rfp: schemas.RFPCreate, structured=None):
    db_obj = models.RFP(title=rfp.title, description=rfp.description, structured=structured)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_rfp(db: Session, rfp_id: int):
    return db.query(models.RFP).filter(models.RFP.id == rfp_id).first()

def list_rfps(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.RFP).offset(skip).limit(limit).all()

def create_vendor(db: Session, vendor: schemas.VendorCreate):
    db_obj = models.Vendor(name=vendor.name, email=vendor.email)
    db.add(db_obj)
    try:
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError as e:
        db.rollback()  # important to reset the session
        # Check for duplicate email error
        if "Duplicate entry" in str(e.orig):
            raise HTTPException(
                status_code=409,
                detail=f"Email {vendor.email} already exists."
            )
        else:
            raise HTTPException(
                status_code=400,
                detail="Database error occurred."
            )
    # db_obj = models.Vendor(name=vendor.name, email=vendor.email)
    # db.add(db_obj)
    # db.commit()
    # db.refresh(db_obj)
    # return db_obj
 
def get_vendor(db: Session, vendor_id: int):
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()

def list_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vendor).offset(skip).limit(limit).all()

def create_proposal(db: Session, vendor_id: int, rfp_id: int, p: schemas.ProposalCreate):
    obj = models.Proposal(
        vendor_id=vendor_id,
        rfp_id=rfp_id,
        proposal=p.proposal,
        raw_email=p.raw_email,
        score=p.score
    )
    print("vendor_id:0---: ",vendor_id)
    db.add(obj)
    db.commit()
    db.refresh(obj)

    print("Created proposal ID:", obj.id)
    # ⚡ Auto-score using compare.py
    final_score = score_proposal(obj)
    print( "Score:", final_score)
    obj.score = final_score

    db.commit()
    db.refresh(obj)
    return obj


def list_proposals_for_rfp(db: Session, rfp_id: int):
    return db.query(models.Proposal).filter(models.Proposal.rfp_id == rfp_id).all()



# CommunicationLog
def create_communication_log(db: Session, vendor_id: int, rfp_id: int, c: schemas.CommunicationLogCreate):

    log = models.CommunicationLog(
        vendor_id=vendor_id,
        rfp_id=rfp_id,
        proposal_id=c.proposal_id,
        direction=c.direction,
        email_type=c.email_type,
        subject=c.subject,
        raw_email=c.raw_email,
        extracted=c.extracted,       # <-- THIS MUST MATCH MODEL FIELD
        status=c.status,
        attempt_count=c.attempt_count,
        reply_received=c.reply_received
    )

    db.add(log)
    db.commit()
    db.refresh(log)
    return log

# ----------------------------
# List CommunicationLogs for a specific RFP
# ----------------------------
def list_communication_logs_for_rfp(db: Session, rfp_id: int):
    return db.query(models.CommunicationLog).filter(
        models.CommunicationLog.rfp_id == rfp_id
    ).order_by(models.CommunicationLog.created_at.desc()).all()


# ----------------------------
# Mark a log as replied
# ----------------------------
def mark_reply_received(db: Session, log_id: int):
    log = db.query(models.CommunicationLog).filter(
        models.CommunicationLog.id == log_id
    ).first()
    if log:
        log.reply_received = True
        log.reply_timestamp = datetime.utcnow()
        log.status = "replied"
        db.commit()
        db.refresh(log)
    return log


# ----------------------------
# Update status of a log (optional)
# ----------------------------
def update_communication_log_status(db: Session, log_id: int, status: str):
    log = db.query(models.CommunicationLog).filter(
        models.CommunicationLog.id == log_id
    ).first()
    if log:
        log.status = status
        db.commit()
        db.refresh(log)
    return log

# crud.py additions

def get_vendor_by_email(db: Session, email: str):
    return db.query(models.Vendor).filter(models.Vendor.email == email).first()

def get_outbound_log(db: Session, vendor_id: int, rfp_id: int):
    return db.query(models.CommunicationLog).filter(
        models.CommunicationLog.vendor_id == vendor_id,
        models.CommunicationLog.rfp_id == rfp_id,
        models.CommunicationLog.direction == "outbound"
    ).first()

def mark_reply_received(db: Session, log_id: int):
    log = db.query(models.CommunicationLog).filter(
        models.CommunicationLog.id == log_id
    ).first()
    if log:
        log.reply_received = True
        log.status = "replied"
        log.reply_timestamp = datetime.utcnow()
        db.commit()
        db.refresh(log)
    return log


def get_best_vendor_for_rfp(db: Session, rfp_id: int):
    # fetch all proposals for this RFP, sorted by score descending
    proposals = (
        db.query(models.Proposal)
          .filter(models.Proposal.rfp_id == rfp_id)
          .order_by(models.Proposal.score.desc())
          .all()
    )

    if not proposals:
        return None

    best = proposals[0]  # highest score
    return best
