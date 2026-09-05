from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.domain import Member
from app.schemas.member import MemberCreate, MemberListResponse, MemberRead

router = APIRouter(prefix="/api/v1/members", tags=["Members"])

@router.get("", response_model=MemberListResponse)
def list_members(db: Session = Depends(get_db)) -> MemberListResponse:
    members = list(db.scalars(select(Member).order_by(Member.member_code)))
    return MemberListResponse(items=[MemberRead.model_validate(item) for item in members], total=len(members))

@router.post("", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberCreate, db: Session = Depends(get_db)) -> MemberRead:
    existing = db.scalar(select(Member).where(Member.member_code == payload.member_code))
    if existing:
        raise HTTPException(status_code=409, detail="Member code already exists")
    member = Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return MemberRead.model_validate(member)

@router.get("/{member_id}", response_model=MemberRead)
def get_member(member_id: str, db: Session = Depends(get_db)) -> MemberRead:
    member = db.get(Member, member_id)
    if not member:
        member = db.scalar(select(Member).where(Member.member_code == member_id))
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return MemberRead.model_validate(member)
