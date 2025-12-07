from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

# ======================
#   RFP SCHEMAS
# ======================

class RFPBase(BaseModel):
    title: str
    description: str
    structured: Optional[Any] = None


class RFPCreate(RFPBase):
    pass


class RFPResponse(RFPBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True  # <-- important


# ======================
#   VENDOR SCHEMAS
# ======================

class VendorBase(BaseModel):
    name: str
    email: str


class VendorCreate(VendorBase):
    pass


class VendorResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True




# ======================
#   PROPOSAL SCHEMAS
# ======================

class ProposalBase(BaseModel):
    vendor_id: int
    rfp_id: int
    proposal: Optional[Any] = None
    raw_email: Optional[str] = None
    score: Optional[int] = None


class ProposalCreate(ProposalBase):
    pass


class ProposalResponse(ProposalBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProposalIn(BaseModel):
    vendor_id: int
    rfp_id: int
    raw_email: str

# ======================
#   NESTED RESPONSE MODELS (OPTIONAL)
# ======================

class ProposalWithRelations(ProposalResponse):
    vendor: VendorResponse
    rfp: RFPResponse


class RFPWithProposals(RFPResponse):
    proposals: List[ProposalResponse] = []


class VendorWithProposals(VendorResponse):
    proposals: List[ProposalResponse] = []



class CommunicationLogBase(BaseModel):
    rfp_id: int
    vendor_id: int
    proposal_id: Optional[int] = None
    direction: str
    email_type: Optional[str] = None
    subject: Optional[str] = None
    raw_email: Optional[str] = None
    extracted: Optional[str]=None
    status: Optional[str] = "pending"
    attempt_count: Optional[int] = 1
    reply_received: Optional[bool] = False

class CommunicationLogCreate(CommunicationLogBase):
    pass

class CommunicationLogResponse(CommunicationLogBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True