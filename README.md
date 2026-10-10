# Cleva Campus Connect: Backend

Backend API for the Cleva Campus Connect platform. Built with **FastAPI** and **Supabase** (Postgres + Supabase Auth).

This file shows what is done, what is coming, and exactly what to send to and expect from each endpoint.

---

## Authentication

1. `POST /auth/login` returns an `access_token`.
2. Send it on every protected request:
   ```
   Authorization: Bearer <access_token>
   ```
3. The backend checks the token and the user's role on every protected request.

There is **no public sign-up**. Accounts are created by an admin in Supabase, so only people with an active row in the `users` table can use the admin API.

### Roles

| Role | Access |
|---|---|
| `super_admin` | Everything, all communities |
| `head_of_campus_leads` | Everything, all communities |
| `campus_lead` | Own community only |
| `ambassador` | Own community only |

Campus leads and ambassadors can view and edit only their own community, and cannot change its `status`.

---

## Endpoint status

| Method | Path | Who | Status |
|---|---|---|---|
| POST | `/auth/login` | Public | Done |
| GET | `/me` | Any logged-in user | Done |
| POST | `/admin/communities` | super_admin, head_of_campus_leads | Done |
| GET | `/admin/communities` | All four roles | Done |
| GET | `/admin/communities/{community_id}` | All four roles (own only for leads and ambassadors) | Done |
| PATCH | `/admin/communities/{community_id}` | All four roles (own only for leads and ambassadors) | Done |
| PATCH | `/admin/communities/{community_id}/archive` | super_admin, head_of_campus_leads | In progress |

Planned: public communities, events, lead profiles, referral challenge, admin dashboard and analytics.

---

## Endpoint reference

### POST `/auth/login`

Public. Rate limit: 5 per minute.

**Request body**

| Field | Type | Required |
|---|---|---|
| `email` | string | Yes |
| `password` | string | Yes |

```json
{ "email": "admin@example.com", "password": "your-password" }
```

**Response 200**
```json
{ "access_token": "eyJhbGciOi..." }
```

**Errors:** 401 wrong email or password, 422 missing field, 429 too many attempts.

---

### GET `/me`

Returns the record of the logged-in user. No request body.

**Response 200**
```json
{
  "user_id": "uuid",
  "auth_id": "uuid",
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "role": "super_admin",
  "status": "active",
  "community_id": null,
  "created_at": "2026-10-10T00:00:00Z",
  "last_login": null
}
```

`role` is one of `super_admin`, `head_of_campus_leads`, `campus_lead`, `ambassador`. `status` is `active` or `inactive`. `community_id` is `null` for the two admin roles and set for campus leads and ambassadors.

**Errors:** 401 bad token, 403 no account or inactive account.

---

### POST `/admin/communities`

Roles: super_admin, head_of_campus_leads.

**Request body**

| Field | Type | Required | Rules |
|---|---|---|---|
| `name` | string | Yes | 1 to 200 characters |
| `school` | string | Yes | 1 to 200 characters |
| `state` | string | Yes | 1 to 100 characters |
| `description` | string | No | Free text |
| `status` | string | No | `active`, `coming_soon`, `temporarily_inactive` or `archived`. Default `coming_soon` |
| `join_link` | string | No | Link to the join page |
| `latitude` | number | No | -90 to 90. Send together with `longitude` |
| `longitude` | number | No | -180 to 180. Send together with `latitude` |

```json
{
  "name": "Cleva Owerri Hub",
  "school": "Federal University of Technology, Owerri",
  "state": "Imo"
}
```

Do not send `community_id`, `slug`, `created_at` or `updated_at`. The backend generates them.

**Response 201:** the full community object (see below).

**Errors:** 401, 403 wrong role, 422 invalid data (for example only one of latitude and longitude), 400 database rejected it.

---

### GET `/admin/communities`

Roles: all four. Campus leads and ambassadors only receive their own community.

**Query parameters**

| Param | Default | Notes |
|---|---|---|
| `q` | none | Searches name, school and state |
| `state` | none | Exact state match |
| `status` | none | One of the status values |
| `page` | 1 | Minimum 1 |
| `page_size` | 20 | 1 to 100 |

Example: `GET /admin/communities?q=owerri&status=active&page=1&page_size=20`

**Response 200**
```json
{
  "items": [ { "...community object..." } ],
  "total": 42,
  "page": 1,
  "page_size": 20
}
```

`total` is the number of matches across all pages. An empty result returns `"items": []` and `"total": 0`.

**Errors:** 401, 403, 422 bad query value (for example `page=0`).

---

### GET `/admin/communities/{community_id}`

Roles: all four (leads and ambassadors only for their own community). No request body.

**Response 200:** the full community object.

**Errors:** 401, 403 not your community, 404 not found, 422 ID is not a valid UUID.

---

### PATCH `/admin/communities/{community_id}`

Roles: all four (leads and ambassadors only for their own community).

**Request body:** every field is optional, with the same types and rules as create (`name`, `school`, `state`, `description`, `status`, `join_link`, `latitude`, `longitude`). Send only what you want to change.

```json
{ "description": "New description" }
```

- An empty body returns 400.
- Slug does not change when the name changes.
- `campus_lead` and `ambassador` get a 403 if they send `status`.

**Response 200:** the full updated community object.

**Errors:** 400 empty body or database rejected it, 401, 403, 404, 422.

---

### PATCH `/admin/communities/{community_id}/archive` (in progress)

Roles: super_admin, head_of_campus_leads. Will set `status` to `archived` instead of deleting. Details will be added when it is built.

---

## Community object

Returned by every communities endpoint.

| Field | Type | Notes |
|---|---|---|
| `community_id` | uuid | Generated by the backend |
| `name` | string | |
| `slug` | string | Generated from the name, unique |
| `school` | string | |
| `state` | string | |
| `description` | string or null | |
| `status` | string | `active`, `coming_soon`, `temporarily_inactive`, `archived` |
| `join_link` | string or null | Hide the join button when `null` |
| `latitude` | number or null | `null` together with `longitude` |
| `longitude` | number or null | |
| `created_at` | datetime | ISO 8601 |
| `updated_at` | datetime | ISO 8601 |

```json
{
  "community_id": "uuid",
  "name": "Cleva Owerri Hub",
  "slug": "cleva-owerri-hub",
  "school": "Federal University of Technology, Owerri",
  "state": "Imo",
  "description": null,
  "status": "coming_soon",
  "join_link": null,
  "latitude": null,
  "longitude": null,
  "created_at": "2026-10-10T00:00:00Z",
  "updated_at": "2026-10-10T00:00:00Z"
}
```


---

## Database

Tables in Supabase (Postgres), all with UUID primary keys: `communities`, `users`, `events`, `leads`, `member_counts`, `referral_entries`, `referral_counts`. Row level security is on.

---



