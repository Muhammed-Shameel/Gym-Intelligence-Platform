from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class MemberCreate(BaseModel):
    member_code: str = Field(min_length=2, max_length=30)
    full_name: str = Field(min_length=2, max_length=160)
    email: EmailStr | None = None
    phone: str | None = None
    joined_on: date
    status: str = "active"
    preferred_training_tags: list[str] = []

class MemberRead(MemberCreate):
    id: str
    model_config = ConfigDict(from_attributes=True)

class MemberListResponse(BaseModel):
    items: list[MemberRead]
    total: int
