from __future__ import annotations
from datetime import date, datetime
from uuid import uuid4

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

def new_id() -> str:
    return str(uuid4())

class Member(Base):
    __tablename__ = "members"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    member_code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str | None] = mapped_column(String(200), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    joined_on: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="active")
    preferred_training_tags: Mapped[list] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    memberships: Mapped[list["Membership"]] = relationship(back_populates="member", cascade="all, delete-orphan")
    attendance_records: Mapped[list["AttendanceRecord"]] = relationship(back_populates="member", cascade="all, delete-orphan")

class Membership(Base):
    __tablename__ = "memberships"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), index=True)
    plan_name: Mapped[str] = mapped_column(String(100))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="active")
    sessions_per_week_target: Mapped[int | None] = mapped_column(Integer, nullable=True)

    member: Mapped["Member"] = relationship(back_populates="memberships")

class AttendanceRecord(Base):
    __tablename__ = "attendance_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), index=True)
    checked_in_at: Mapped[datetime] = mapped_column(DateTime, index=True)
    source: Mapped[str] = mapped_column(String(30), default="manual")

    member: Mapped["Member"] = relationship(back_populates="attendance_records")

class Trainer(Base):
    __tablename__ = "trainers"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    trainer_code: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(160))
    skill_tags: Mapped[list] = mapped_column(JSON, default=list)
    max_active_members: Mapped[int] = mapped_column(Integer, default=20)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class TrainerAvailability(Base):
    __tablename__ = "trainer_availability"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    trainer_id: Mapped[str] = mapped_column(ForeignKey("trainers.id"), index=True)
    available_date: Mapped[date] = mapped_column(Date)
    available_slots: Mapped[int] = mapped_column(Integer, default=0)

class TrainerAssignment(Base):
    __tablename__ = "trainer_assignments"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), index=True)
    trainer_id: Mapped[str] = mapped_column(ForeignKey("trainers.id"), index=True)
    assigned_on: Mapped[date] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(30), default="active")

class FollowUpActivity(Base):
    __tablename__ = "follow_up_activities"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    member_id: Mapped[str] = mapped_column(ForeignKey("members.id"), index=True)
    activity_type: Mapped[str] = mapped_column(String(40))
    occurred_at: Mapped[datetime] = mapped_column(DateTime)
    outcome: Mapped[str] = mapped_column(String(60))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

class WorkflowSession(Base):
    __tablename__ = "workflow_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    workflow_session_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    member_id: Mapped[str] = mapped_column(String(36), index=True)
    review_reason: Mapped[str] = mapped_column(String(60), default="general_review")
    status: Mapped[str] = mapped_column(String(30), default="created")
    input_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    context_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    final_output_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

class AgentExecutionLog(Base):
    __tablename__ = "agent_execution_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    workflow_session_id: Mapped[str] = mapped_column(String(40), index=True)
    agent_name: Mapped[str] = mapped_column(String(100))
    sequence_number: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30))
    input_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    output_summary: Mapped[dict] = mapped_column(JSON, default=dict)
    rules_triggered: Mapped[list] = mapped_column(JSON, default=list)
    context_updated: Mapped[list] = mapped_column(JSON, default=list)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    error_details: Mapped[str | None] = mapped_column(Text, nullable=True)

class DecisionRecord(Base):
    __tablename__ = "decision_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    decision_id: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    audit_reference: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    workflow_session_id: Mapped[str] = mapped_column(String(40), index=True)
    member_id: Mapped[str] = mapped_column(String(36), index=True)
    final_classification: Mapped[str | None] = mapped_column(String(60), nullable=True)
    final_score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    reason_codes: Mapped[list] = mapped_column(JSON, default=list)
    evidence_snapshot: Mapped[dict] = mapped_column(JSON, default=dict)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
