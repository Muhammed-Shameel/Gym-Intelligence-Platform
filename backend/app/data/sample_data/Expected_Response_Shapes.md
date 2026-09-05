# GFIP API Contract Guide

## Foundation Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Health check |
| GET | `/api/v1/members` | List members |
| POST | `/api/v1/members` | Create demo member |
| GET | `/api/v1/members/{member_id}` | Member detail |
| GET | `/api/v1/trainers` | List trainers |

## Intelligence Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/reviews/member` | Run deterministic member review |
| GET | `/api/v1/workflows/{workflow_session_id}` | Retrieve workflow session |
| GET | `/api/v1/workflows/{workflow_session_id}/context` | Inspect shared context |
| GET | `/api/v1/workflows/{workflow_session_id}/trace` | Retrieve agent trace |
| GET | `/api/v1/audit/{audit_reference}` | Retrieve decision audit |
| GET | `/api/v1/dashboard/summary` | Dashboard summary |

## Review Request

```json
{
  "member_id": "MEM-002",
  "review_reason": "renewal_review"
}
```

## Review Response Shape

```json
{
  "workflow_session_id": "WF-000001",
  "member_id": "MEM-002",
  "status": "completed",
  "engagement": {
    "score": 75,
    "category": "High Risk"
  },
  "renewal": {
    "score": 85,
    "priority": "Urgent"
  },
  "trainer": {
    "recommendation": "retain_current",
    "trainer_id": "TRN-001"
  },
  "next_action": {
    "action": "trainer_and_renewal_call",
    "due_hours": 24
  },
  "reason_codes": [],
  "agent_trace": [],
  "explanation": "",
  "audit_reference": "AUD-000001"
}
```

## Error Behavior

- 404 for unknown member
- 422 for invalid request
- Controlled `insufficient_data` result when member exists but records are insufficient
- No successful recommendation may be fabricated
