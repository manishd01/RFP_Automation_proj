from typing import List, Dict, Any
from sqlalchemy.orm import Session
from . import models
import math

def _extract_numeric(proposal_json: Dict[str,Any], keys):
    # try to get number values from a few possible keys
    for k in keys:
        v = proposal_json.get(k)
        if isinstance(v, (int,float)):
            return float(v)
        if isinstance(v, str):
            try:
                return float(v.replace(',',''))
            except:
                pass
    return None

def score_proposal(proposal: models.Proposal) -> float:
    # If explicit score present, use it (but normalize)
    if proposal.score is not None:
        return float(proposal.score)
    p = proposal.proposal or {}
    # Try price (lower is better) and delivery_days (lower better), quality (higher better)
    price = _extract_numeric(p, ["price", "cost", "total", "amount"])
    delivery = _extract_numeric(p, ["delivery_days", "lead_time", "delivery"])
    quality = _extract_numeric(p, ["quality_score", "rating", "score"])
    # Base score
    score = 0.0
    if quality is not None:
        score += quality * 10
    if price is not None:
        # invert price so cheaper -> higher; avoid divide by zero
        score += 1000.0 / (price + 1.0)
    if delivery is not None:
        score += max(0.0, 50.0 - delivery)
    # fallback if everything missing: use created_at timestamp recency
    if score == 0.0:
        # use epoch seconds mod to produce deterministic value
        score = float(proposal.created_at.timestamp() % 100)
    # round
    return round(score, 2)

def compare_rfp(db: Session, rfp_id: int):
    proposals = db.query(models.Proposal).filter(models.Proposal.rfp_id==rfp_id).all()
    ranked = []
    for p in proposals:
        s = score_proposal(p)
        ranked.append({
            "proposal_id": p.id,
            "vendor_id": p.vendor_id,
            "vendor_name": p.vendor.name if p.vendor else None,
            "score": s,
            "raw": p.proposal
        })
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return {"rfp_id": rfp_id, "ranked": ranked}
