from sqlalchemy.orm import Session
from app.models.domain import Member, Membership, AttendanceRecord, TrainerAssignment, FollowUpActivity
from app.services.context.base import SharedWorkflowContext

class ContextBuilder:
    def __init__(self, db: Session):
        self.db = db

    def build_context(self, session_id: str, member_id: str) -> SharedWorkflowContext:
        member = self.db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise ValueError(f"Member with ID {member_id} not found.")

        # Fetch related data
        membership = self.db.query(Membership).filter(Membership.member_id == member_id, Membership.status == "active").first()
        attendance = self.db.query(AttendanceRecord).filter(AttendanceRecord.member_id == member_id).order_by(AttendanceRecord.checked_in_at.desc()).limit(10).all()
        trainer_assignment = self.db.query(TrainerAssignment).filter(TrainerAssignment.member_id == member_id, TrainerAssignment.status == "active").first()
        follow_ups = self.db.query(FollowUpActivity).filter(FollowUpActivity.member_id == member_id).order_by(FollowUpActivity.occurred_at.desc()).limit(5).all()

        # Convert to dicts (very simple conversion for now, can be improved)
        member_dict = {"id": member.id, "full_name": member.full_name, "status": member.status}
        membership_dict = {"plan": membership.plan_name} if membership else {}
        attendance_list = [{"checked_in_at": str(a.checked_in_at)} for a in attendance]
        trainer_dict = {"trainer_id": trainer_assignment.trainer_id} if trainer_assignment else {}
        follow_up_list = [{"activity": f.activity_type} for f in follow_ups]

        return SharedWorkflowContext.create_scoped_context(
            session_id=session_id,
            member_id=member_id,
            member_profile=member_dict,
            active_membership=membership_dict,
            attendance_summary={"records": attendance_list},
            trainer_assignment=trainer_dict,
            follow_up_summary={"activities": follow_up_list}
        )
