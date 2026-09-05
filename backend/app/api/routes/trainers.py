from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.database import get_db
from app.models.domain import Trainer

router = APIRouter(prefix="/api/v1/trainers", tags=["Trainers"])

class TrainerCreate(BaseModel):
    trainer_code: str
    full_name: str
    skill_tags: list[str] = Field(default_factory=list)
    max_active_members: int = 20
    active: bool = True

class TrainerRead(TrainerCreate):
    id: str

@router.get("", response_model=dict)
def list_trainers(db: Session = Depends(get_db)) -> dict:
    trainers = list(db.scalars(select(Trainer).order_by(Trainer.trainer_code)))
    return {
        "items": [
            {
                "id": item.id,
                "trainer_code": item.trainer_code,
                "full_name": item.full_name,
                "skill_tags": item.skill_tags,
                "max_active_members": item.max_active_members,
                "active": item.active,
            }
            for item in trainers
        ],
        "total": len(trainers),
    }

@router.post("", response_model=TrainerRead, status_code=status.HTTP_201_CREATED)
def create_trainer(payload: TrainerCreate, db: Session = Depends(get_db)) -> TrainerRead:
    existing = db.scalar(select(Trainer).where(Trainer.trainer_code == payload.trainer_code))
    if existing:
        raise HTTPException(status_code=409, detail="Trainer code already exists")
    trainer = Trainer(**payload.model_dump())
    db.add(trainer)
    db.commit()
    db.refresh(trainer)
    return TrainerRead(
        id=trainer.id,
        trainer_code=trainer.trainer_code,
        full_name=trainer.full_name,
        skill_tags=trainer.skill_tags,
        max_active_members=trainer.max_active_members,
        active=trainer.active
    )
