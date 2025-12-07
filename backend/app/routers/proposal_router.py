from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..deps import get_db

router = APIRouter()

@router.get('/for_rfp/{rfp_id}')
async def list_for_rfp(rfp_id: int, db: Session = Depends(get_db)):
    props = crud.list_proposals_for_rfp(db, rfp_id)
    # simple serialization
    return [ {
        'id': p.id,
        'vendor_id': p.vendor_id,
        'rfp_id': p.rfp_id,
        'proposal': p.proposal,
        'score': p.score
    } for p in props ]

@router.post('/{vendor_id}/{rfp_id}')
async def create_proposal(
    vendor_id: int,
    rfp_id: int,
    payload: schemas.ProposalCreate,
    db: Session = Depends(get_db)
):
    print("vendor if from router: --------------- ", vendor_id)
    obj = crud.create_proposal(db, vendor_id, rfp_id, payload)
    return {
        'id': obj.id,
        'vendor_id': obj.vendor_id,
        'rfp_id': obj.rfp_id,
        'proposal': obj.proposal,
        'score': obj.score,
        'created_at': obj.created_at
    }
