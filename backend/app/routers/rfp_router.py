from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..deps import get_db
from ..services.ai_service import  *
router = APIRouter()

''' Example RFP description text:

We need to procure the following items for our new office:

1. Item Name: Laptop
   Quantity: 20
   Type: Desktop Hardware
   Processor: Intel Core i7
   RAM: 16GB
   Storage: SSD 512GB

2. Item Name: Monitor
   Quantity: 15
   Type: Desktop Hardware
   Processor: N/A
   RAM: N/A
   Storage: N/A
   Size: 27-inch

Budget: 50,000
Timeline: 30 days
Payment Terms: Net 30
Warranty: At least 1 year for all items
Evaluation Criteria: Quality, Warranty, Delivery Timelines

'''
@router.post("/", response_model=schemas.RFPResponse)
async def create_rfp(rfp_in: schemas.RFPCreate, db: Session = Depends(get_db)):
    # 1. Full text from user
    # paragraph = rfp_in.description

    # # 2. AI extraction
    # structured = extract_structured_from_text(paragraph)
    print("RFP old:", type(rfp_in.description))
    print("RFP old:", rfp_in.description)
    # If receiving raw string (not recommended)
    paragraph = rfp_in.description                      
    structured = extract_structured_from_text(paragraph)
    print("Structured RFP:", structured)
    created = crud.create_rfp(db, rfp_in, structured=structured)
    return created

@router.get("/", response_model=list[schemas.RFPResponse])
async def list_rfps(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.list_rfps(db, skip=skip, limit=limit)

@router.get("/{rfp_id}", response_model=schemas.RFPResponse)
async def get_rfp(rfp_id: int, db: Session = Depends(get_db)):
    r = crud.get_rfp(db, rfp_id)
    if not r:
        raise HTTPException(status_code=404, detail="RFP not found")
    return r


@router.get("/best-proposal/{rfp_id}")
def get_best_proposal(rfp_id: int, db: Session = Depends(get_db)):

    best = crud.get_best_vendor_for_rfp(db, rfp_id)

    if not best:
        return {"message": "No proposals found for this RFP."}

    return {
        "rfp_id": best.rfp_id,
        "vendor_id": best.vendor_id,
        "proposal_id": best.id,
        "score": best.score,
        "created_at": best.created_at,
        "proposal": best.proposal
    }
