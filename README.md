# Cleva Campus Connect

A responsive web platform connecting Cleva with students, campus communities, events, and ambassador-led growth across Nigeria.

Built by **Team 4 · Cleva Ambassadors Program**.

## What it does

- **Public site (no sign-in):** find campus communities by institution, state, or name; browse events; view approved campus lead profiles; learn about the ambassador journey; submit the referral challenge form.
  
- **Admin workspace (role-protected):** private dashboard for the head of campus leads and authorised operators to view communities, events, referrals, member counts, leaderboards, and growth over time.

Out of scope: social feed, messaging, payments, ticketing, in-app ambassador applications, native mobile apps.

## Repository structure

```
cleva-campus-connect/
backend/     API, database, authentication, role checks
frontend/    Web app (mobile-first)
docs/        PRD, database design, API notes
README.md
```

## Tech stack

To be confirmed.

| Part | Choice |
|---|---|
| Backend | TBD |
| Database | PostgreSQL |
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


### 3. events
`event_id` (PK), `community_id` (FK), `title`, `slug`, `description`, `start_time`, `venue`, `signup_link`, `status`, `created_at`, `updated_at`


### 4. leads
`lead_id`, `community_id`, `full_name`, `role`, `bio`, `photo`, `links`, `status`


### 5. referral_entries
`entry_id`, `community_id` (optional), `cleva_tag`, `full_name`, `state`, `status`, `consent_version`, `submitted_at`

What people submit on the referral challenge form. 

### 6. referral_counts
`referral_count_id`, `entry_id`, `total`, `period`, `source`, `status`, `fetched_at`



### 7. member_counts
`member_count_id`, `community_id`, `total`, `source`, `recorded_at`


### Relationships

```
communities  < users            (optional)
             < events
             < leads
             < member_counts
             < referral_entries (optional) < referral_counts
```

