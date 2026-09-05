# GFIP Data Model and Data Dictionary

## Core Relationships

```text
Member 1 ── * Membership
Member 1 ── * AttendanceRecord
Member 1 ── * TrainerAssignment
Trainer 1 ── * TrainerAssignment
Trainer 1 ── * TrainerAvailability
Member 1 ── * FollowUpActivity
Member 1 ── * WorkflowSession
WorkflowSession 1 ── * AgentExecutionLog
WorkflowSession 1 ── 0..1 DecisionRecord
```

## Entities

### Member

| Field | Type | Rules |
|---|---|---|
| id | UUID/string | Primary key |
| member_code | string | Unique |
| full_name | string | Fictional demo name |
| email | string | Optional fictional value |
| phone | string | Optional fictional value |
| joined_on | date | Required |
| status | string | active, paused, inactive |
| preferred_training_tags | JSON/list | Approved operational tags |
| created_at | datetime | Audit field |

### Membership

| Field | Type | Rules |
|---|---|---|
| id | UUID/string | Primary key |
| member_id | FK | Required |
| plan_name | string | Required |
| start_date | date | Required |
| end_date | date | Required |
| status | string | active, expired, cancelled |
| sessions_per_week_target | integer | Optional planning field |

### AttendanceRecord

| Field | Type | Rules |
|---|---|---|
| id | UUID/string | Primary key |
| member_id | FK | Required |
| checked_in_at | datetime | Required |
| source | string | manual, kiosk, import |

### Trainer

| Field | Type | Rules |
|---|---|---|
| id | UUID/string | Primary key |
| trainer_code | string | Unique |
| full_name | string | Required |
| skill_tags | JSON/list | Approved tags only |
| max_active_members | integer | Positive |
| active | boolean | Required |

### TrainerAvailability

| Field | Type | Rules |
|---|---|---|
| id | UUID/string | Primary key |
| trainer_id | FK | Required |
| available_date | date | Required |
| available_slots | integer | Non-negative |

### TrainerAssignment

| Field | Type | Rules |
|---|---|---|
| id | UUID/string | Primary key |
| member_id | FK | Required |
| trainer_id | FK | Required |
| assigned_on | date | Required |
| status | string | active, ended |

### FollowUpActivity

| Field | Type | Rules |
|---|---|---|
| id | UUID/string | Primary key |
| member_id | FK | Required |
| activity_type | string | call, message, in_person |
| occurred_at | datetime | Required |
| outcome | string | contacted, no_response, planned |
| notes | string | No sensitive health notes |

### WorkflowSession

Stores one review execution, input snapshot, status, and output snapshot.

### AgentExecutionLog

Stores sequence, agent, status, rules, evidence, context updates, and timing.

### DecisionRecord

Stores final classification, scores, recommendation, reason codes, evidence, explanation, and audit reference.
