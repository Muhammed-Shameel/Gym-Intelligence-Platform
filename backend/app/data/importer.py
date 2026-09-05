import os
import csv
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.domain import Member, Membership, AttendanceRecord, Trainer, FollowUpActivity

# Use path relative to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "app/data/sample_data")

def import_csv_data(db: Session):
    # 1. Members
    with open(f"{DATA_DIR}/members.csv", mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row['member_code'].startswith('MEM-'):
                continue
            member = Member(
                member_code=row['member_code'],
                full_name=row['full_name'],
                joined_on=datetime.strptime(row['joined_on'], '%Y-%m-%d').date(),
                status=row['status'],
                preferred_training_tags=row['preferred_training_tags'].split('|') if row['preferred_training_tags'] else []
            )
            db.add(member)
    db.commit()

    # 2. Trainers
    with open(f"{DATA_DIR}/trainers.csv", mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trainer = Trainer(
                trainer_code=row['trainer_code'],
                full_name=row['full_name'],
                skill_tags=row['skill_tags'].split('|') if row['skill_tags'] else [],
                max_active_members=int(row['max_active_members']),
                active=row['active'] == 'True'
            )
            db.add(trainer)
    db.commit()
    
    # Mapping for lookups
    member_map = {m.member_code: m.id for m in db.query(Member).all()}

    # 3. Memberships
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
    db.commit()

    # 4. Attendance
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
    db.commit()

    # 5. Follow-ups
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
    print("Data imported successfully from CSVs.")
