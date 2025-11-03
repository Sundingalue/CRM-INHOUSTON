from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models import Agent
from app.schemas import AgentCreate, AgentOut

router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("", response_model=AgentOut)
def create_agent(body: AgentCreate, db: Session = Depends(get_db)):
    agent = Agent(**body.dict())
    db.add(agent)
    db.commit()
    db.refresh(agent)
    return agent

@router.get("", response_model=List[AgentOut])
def list_agents(tenant_id: int, db: Session = Depends(get_db)):
    return db.query(Agent).filter(Agent.tenant_id == tenant_id).all()

@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent
