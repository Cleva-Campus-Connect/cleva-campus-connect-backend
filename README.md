# Cleva Campus Connect

A responsive web platform connecting Cleva with students, campus communities, events, and ambassador-led growth across Nigeria.

Built by **Team 4 Â· Cleva Ambassadors Program**.

> Status: early development. The product requirements are in [`docs/`](docs/) (Cleva Campus Connect PRD v1.0). Nothing here is confirmation that Cleva has approved the scope, API access, brand assets, or production data.

## What it does

- **Public site (no sign-in):** find campus communities by institution, state, or name; browse events; view approved campus lead profiles; learn about the ambassador journey; submit the referral challenge form.
- **Admin workspace (role-protected):** private dashboard for the head of campus leads and authorised operators to view communities, events, referrals, member counts, leaderboards, and growth over time.

Out of scope: social feed, messaging, payments, ticketing, in-app ambassador applications, native mobile apps.

## Repository structure

```
cleva-campus-connect/
â”œâ”€â”€ backend/     API, database, authentication, role checks
â”œâ”€â”€ frontend/    Web app (mobile-first)
â”œâ”€â”€ docs/        PRD, database design, API notes
â””â”€â”€ README.md
```

## Tech stack

To be confirmed.

| Part | Choice |
|---|---|
| Backend | TBD |
| Database | PostgreSQL |
| Authentication | TBD |
| Frontend | TBD |

## Roles and access

Access is checked on the server for every protected request, not only hidden in the UI.

| Role | Community | Access |
|---|---|---|
| Super Admin | None | Everything: records, roles, settings |
| Head of Campus Leads | None | All communities, events, leads, referrals, analytics |
| Campus Lead | Required | Their own community's events, leads, and ambassadors |
| Ambassador | Required | Their own community's events and details |

Students use the public site and do not have accounts.

## Database design

Seven tables. Everything connects to `communities`, except referral counts, which belong to referral entries.

### 1. users
`user_id`, `full_name`, `email`, `role`, `status`, `community_id`, `created_at`, `last_login`

`community_id` is required for Campus Leads and Ambassadors, and empty for Super Admin and Head of Campus Leads.

### 2. communities
`community_id` (PK), `name`, `slug`, `school`, `description`, `status`, `join_link`, `latitude`, `longitude`, `created_at`, `updated_at`

Communities with no coordinates stay in list results with "Map location unavailable".

### 3. events
`event_id` (PK), `community_id` (FK), `title`, `slug`, `description`, `start_time`, `venue`, `signup_link`, `status`, `created_at`, `updated_at`

An event with no venue is online. Times are shown in WAT (UTC+1).

### 4. leads
`lead_id`, `community_id`, `full_name`, `role`, `bio`, `photo`, `links`, `status`

Public profiles only. No private contact details are stored or published.

### 5. referral_entries
`entry_id`, `community_id` (optional), `cleva_tag`, `full_name`, `state`, `status`, `consent_version`, `submitted_at`

What people submit on the referral challenge form. The Cleva tag is unique, so repeated submissions do not create duplicates.

### 6. referral_counts
`referral_count_id`, `entry_id`, `total`, `period`, `source`, `status`, `fetched_at`

Numbers fetched from Cleva. Each fetch adds a new row. `total` is empty when unavailable, never zero. `source` marks sample data (`mock`) clearly until the real Cleva integration is tested.

### 7. member_counts
`member_count_id`, `community_id`, `total`, `source`, `recorded_at`

Membership snapshots over time. `total` is empty when unknown, and `source` says whether the number is reported, estimated, or verified.

### Relationships

```
communities â”€â”¬â”€< users            (optional)
             â”œâ”€< events
             â”œâ”€< leads
             â”œâ”€< member_counts
             â””â”€< referral_entries (optional) â”€< referral_counts
```

### Data rules
- Records are archived through `status`, not deleted.
- Unknown, unavailable, and zero are never mixed up. Missing numbers stay empty.
- Mock or sample data is always labelled.
- Referral entries and exports are restricted to authorised roles.
- Names and Cleva tags are never sent to general analytics or logs.

### Still to be designed
`clicks` (join and signup link intent) and `activity_log` (admin actions).

## Getting started

Setup instructions will be added once the stack is chosen.

## Contributing

- `main` is protected. Open a pull request for every change.
- Branch names: `backend/<topic>` or `frontend/<topic>`, for example `backend/users-table`.
- Never commit secrets. Keep credentials in `.env` files, which are ignored by git.
- If implementation conflicts with the PRD, raise it and record the decision rather than changing scope silently.

## Documents

- Cleva Campus Connect PRD v1.0 (`docs/`)
- Backend design requirements (`docs/`)
