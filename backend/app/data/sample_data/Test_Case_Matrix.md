# GFIP Validation Scenario Pack

## Scenario 1 — Active Member

- Recent attendance
- Stable 30-day visits
- Membership expiry beyond 30 days
- Recent follow-up
- Suitable active trainer

Expected: Active, low renewal priority, retain trainer, normal engagement action.

## Scenario 2 — High-Risk Renewal

- Last attendance 21+ days ago
- Low 30-day visits
- Membership expires within 7 days
- No follow-up in 14 days

Expected: High Risk, Urgent renewal, contact within 24 hours.

## Scenario 3 — Attendance Decline

- Recent visit exists
- Current 30-day attendance is at least 50% below prior period

Expected: Watch or At Risk depending total score; evidence shows decline.

## Scenario 4 — Trainer Unavailable

- Member is assigned
- Current trainer is inactive or unavailable
- Alternative trainer has matching skill and lower load

Expected: Human-reviewed trainer alternative recommendation.

## Scenario 5 — Insufficient Data

- New member
- Fewer than two reliable attendance records

Expected: Insufficient Data; verify records; no unsupported risk conclusion.

## Scenario 6 — Unknown Member

Expected: Controlled 404 or not-found response; no agents fabricate output.

## Scenario 7 — Invalid Request

Missing member ID.

Expected: 422 validation error.

## Scenario 8 — Conflicting Signals

- Active attendance
- Membership expires within 7 days

Expected: Engagement remains Active while renewal priority is High/Urgent. The aggregator preserves both dimensions.
