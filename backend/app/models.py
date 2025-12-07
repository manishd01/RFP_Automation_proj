from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship, declarative_base
import datetime

Base = declarative_base()

class RFP(Base):
    __tablename__ = "rfps"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    structured = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    proposals = relationship("Proposal", back_populates="rfp")

class Vendor(Base):
    __tablename__ = "vendors"
    id = Column(Integer,primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)

    proposals = relationship("Proposal", back_populates="vendor")

class Proposal(Base):
    __tablename__ = "proposals"
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    rfp_id = Column(Integer, ForeignKey("rfps.id"))
    proposal = Column(JSON, nullable=True)
    raw_email = Column(Text, nullable=True)
    score = Column(Integer, nullable=True  ) 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    vendor = relationship("Vendor", back_populates="proposals")
    rfp = relationship("RFP", back_populates="proposals")
 


class CommunicationLog(Base):
    __tablename__ = "communication_logs"

    id = Column(Integer, primary_key=True, index=True)

    rfp_id = Column(Integer, ForeignKey("rfps.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=True)

    direction = Column(String(20), nullable=False)  
    email_type = Column(String(50), nullable=True)  
    attempt_count = Column(Integer, default=1)

    subject = Column(String(255), nullable=True)
    raw_email = Column(Text, nullable=True)
    extracted = Column(JSON, nullable=True)

    reply_received = Column(Boolean, default=False)
    reply_timestamp = Column(DateTime, nullable=True)

    status = Column(String(50), default="pending")  
    processing_notes = Column(Text, nullable=True)

    message_id = Column(String(255), nullable=True)  
    attachments = Column(JSON, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    vendor = relationship("Vendor")
    rfp = relationship("RFP")
    proposal = relationship("Proposal")




    #  alembic revision --autogenerate -m "added communiation log table for comapriion logic"
    # alembic upgrade head