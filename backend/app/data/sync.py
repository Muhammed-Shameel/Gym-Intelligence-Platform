import os
import csv
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.domain import Member, Membership, AttendanceRecord, Trainer, FollowUpActivity

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "sample_data")

def sync_data():
    db = SessionLocal()
    try:
        # 1. Upsert Members
        with open(f"{DATA_DIR}/members.csv", mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                member = db.query(Member).filter(Member.member_code == row['member_code']).first()
                if member:
                    member.full_name = row['full_name']
                    member.status = row['status']
                    member.preferred_training_tags = row['preferred_training_tags'].split('|')
                else:
                    member = Member(
                        member_code=row['member_code'],
                        full_name=row['full_name'],
                        joined_on=datetime.strptime(row['joined_on'], '%Y-%m-%d').date(),
                        status=row['status'],
                        preferred_training_tags=row['preferred_training_tags'].split('|')
                    )
                    db.add(member)
        db.commit()

        # 2. Upsert Trainers
        with open(f"{DATA_DIR}/trainers.csv", mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                trainer = db.query(Trainer).filter(Trainer.trainer_code == row['trainer_code']).first()
                if trainer:
                    trainer.full_name = row['full_name']
                    trainer.skill_tags = row['skill_tags'].split('|')
                    trainer.max_active_members = int(row['max_active_members'])
                    trainer.active = row['active'] == 'True'
                else:
                    trainer = Trainer(
                        trainer_code=row['trainer_code'],
                        full_name=row['full_name'],
                        skill_tags=row['skill_tags'].split('|'),
                        max_active_members=int(row['max_active_members']),
                        active=row['active'] == 'True'
                    )
                    db.add(trainer)
        db.commit()

        # 3. Clear and Re-import dependent data to keep clean
        db.query(Membership).delete()
        db.query(AttendanceRecord).delete()
        db.query(FollowUpActivity).delete()
        db.commit()

        member_map = {m.member_code: m.id for m in db.query(Member).all()}

        # Re-import Memberships
        with open(f"{DATA_DIR}/memberships.csv", mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['member_code'] in member_map:
                    membership = Membership(
                        member_id=member_map[row['member_code']],
                        plan_name=row['plan_name'],
                        start_date=datetime.strptime(row['start_date'], '%Y-%m-%d').date(),
                        end_date=datetime.strptime(row['end_date'], '%Y-%m-%d').date(),
                        status=row['status'],
                        sessions_per_week_target=int(row['sessions_per_week_target']) if row['sessions_per_week_target'] else None
                    )
                    db.add(membership)

        # Re-import Attendance
        with open(f"{DATA_DIR}/attendance_records.csv", mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['member_code'] in member_map:
                    attendance = AttendanceRecord(
                        member_id=member_map[row['member_code']],
                        checked_in_at=datetime.strptime(row['checked_in_at'], '%Y-%m-%dT%H:%M:%S'),
                        source=row['source']
                    )
                    db.add(attendance)

        # Re-import Follow-ups
        with open(f"{DATA_DIR}/follow_up_activities.csv", mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['member_code'] in member_map:
                    followup = FollowUpActivity(
                        member_id=member_map[row['member_code']],
                        activity_type=row['activity_type'],
                        occurred_at=datetime.strptime(row['occurred_at'], '%Y-%m-%dT%H:%M:%S'),
                        outcome=row['outcome'],
                        notes=row['notes']
                    )
                    db.add(followup)
        db.commit()
        print("Database synchronization complete.")
    except Exception as e:
        print(f"Sync error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    sync_data()
