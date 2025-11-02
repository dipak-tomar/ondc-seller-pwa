from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.models import PricingRule, Store
from app.db.base import get_db
from app.routes.auth import get_current_user_id
from datetime import datetime

router = APIRouter(prefix="/pricing-rules", tags=["pricing-rules"])

def get_user_store_id(user_id: str, db: Session) -> str:
    store = db.query(Store).filter(Store.user_id == user_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store.id

class PricingRuleCreate(BaseModel):
    name: str
    rule_type: str
    discount_percentage: float
    conditions: dict

class PricingRuleResponse(BaseModel):
    id: str
    store_id: str
    name: str
    rule_type: str
    discount_percentage: float
    conditions: dict
    is_active: bool
    created_at: datetime

@router.get("", response_model=List[PricingRuleResponse])
async def list_pricing_rules(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    rules = db.query(PricingRule).filter(PricingRule.store_id == store_id).all()
    
    return [PricingRuleResponse(
        id=r.id,
        store_id=r.store_id,
        name=r.name,
        rule_type=r.rule_type,
        discount_percentage=r.discount_percentage,
        conditions=r.conditions,
        is_active=r.is_active,
        created_at=r.created_at
    ) for r in rules]

@router.post("", response_model=PricingRuleResponse)
async def create_pricing_rule(
    rule: PricingRuleCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    new_rule = PricingRule(
        store_id=store_id,
        name=rule.name,
        rule_type=rule.rule_type,
        discount_percentage=rule.discount_percentage,
        conditions=rule.conditions
    )
    
    db.add(new_rule)
    db.commit()
    db.refresh(new_rule)
    
    return PricingRuleResponse(
        id=new_rule.id,
        store_id=new_rule.store_id,
        name=new_rule.name,
        rule_type=new_rule.rule_type,
        discount_percentage=new_rule.discount_percentage,
        conditions=new_rule.conditions,
        is_active=new_rule.is_active,
        created_at=new_rule.created_at
    )

@router.delete("/{rule_id}")
async def delete_pricing_rule(
    rule_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    rule = db.query(PricingRule).filter(PricingRule.id == rule_id).first()
    
    if not rule:
        raise HTTPException(status_code=404, detail="Pricing rule not found")
    
    if rule.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db.delete(rule)
    db.commit()
    
    return {"message": "Pricing rule deleted"}
