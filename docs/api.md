# API Endpoints

Base path: `/api/v1`

---

## Candidates

### `GET /api/v1/candidates/`

List candidates with pagination.

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `offset` | int | 0 | Skip N records |
| `limit` | int | 100 | Max records to return |

**Response** `200`: `list[CandidateRead]`

---

### `GET /api/v1/candidates/{candidate_id}`

Get a single candidate by ID.

**Response** `200`: `CandidateRead`
**Error** `404`: Candidate not found

---

### `POST /api/v1/candidates/`

Create a new candidate.

**Body** `CandidateCreate`:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | yes | 1–255 chars |
| `email` | string (email) | yes | Valid email format |
| `skills` | string[] | no | Defaults to `[]` |
| `experience` | int | no | `>= 0`, years of experience |
| `resume_url` | string | no | URL to resume |

**Response** `201`: `CandidateRead`
**Error** `409`: Email already exists

---

### `PATCH /api/v1/candidates/{candidate_id}`

Partially update a candidate. Only provided fields are changed. Sending `null` clears the field.

**Body** `CandidateUpdate` (all fields optional):

| Field | Type | Constraints |
|-------|------|-------------|
| `name` | string \| null | 1–255 chars |
| `email` | string (email) \| null | Valid email format |
| `skills` | string[] \| null | |
| `experience` | int \| null | `>= 0` |
| `resume_url` | string \| null | |

**Response** `200`: `CandidateRead`
**Error** `404`: Candidate not found
**Error** `409`: Email already taken by another candidate

---

### `DELETE /api/v1/candidates/{candidate_id}`

Delete a candidate.

**Response** `204`: No content
**Error** `404`: Candidate not found

---

## Jobs

### `GET /api/v1/jobs/`

List jobs with pagination.

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `offset` | int | 0 | Skip N records |
| `limit` | int | 100 | Max records to return |

**Response** `200`: `list[JobRead]`

---

### `GET /api/v1/jobs/{job_id}`

Get a single job by ID.

**Response** `200`: `JobRead`
**Error** `404`: Job not found

---

### `POST /api/v1/jobs/`

Create a new job.

**Body** `JobCreate`:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `title` | string | yes | 1–255 chars |
| `description` | string | no | Free text |
| `requirements` | string[] | no | Defaults to `[]` |
| `location` | string | no | |
| `salary_range` | string | no | |

**Response** `201`: `JobRead`

---

### `PATCH /api/v1/jobs/{job_id}`

Partially update a job. Only provided fields are changed. Sending `null` clears the field.

**Body** `JobUpdate` (all fields optional):

| Field | Type | Constraints |
|-------|------|-------------|
| `title` | string \| null | 1–255 chars |
| `description` | string \| null | |
| `requirements` | string[] \| null | |
| `location` | string \| null | |
| `salary_range` | string \| null | |

**Response** `200`: `JobRead`
**Error** `404`: Job not found

---

### `DELETE /api/v1/jobs/{job_id}`

Delete a job.

**Response** `204`: No content
**Error** `404`: Job not found

---

## Evaluations

### `POST /api/v1/evaluations/`

Create an evaluation for a candidate-job pair. The LLM analysis runs **asynchronously** in the background.

If an evaluation already exists for the same `candidate_id` + `job_id` pair, the existing record is returned without creating a duplicate. If the existing evaluation is `failed`, it is reset and reprocessed.

**Body** `EvaluationCreate`:

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `candidate_id` | int | yes | `> 0`, must reference an existing candidate |
| `job_id` | int | yes | `> 0`, must reference an existing job |

**Response** `201`: `EvaluationRead` (initially with `status: "pending"`)

Poll `GET /api/v1/evaluations/{id}` to check when `status` becomes `"completed"` or `"failed"`.

**Error** `409`: Integrity constraint violation (e.g., candidate or job does not exist)

---

### `GET /api/v1/evaluations/{evaluation_id}`

Get an evaluation by ID, including its current processing status and results.

**Response** `200`: `EvaluationRead`
**Error** `404`: Evaluation not found

---

## Health

### `GET /health`

Health check endpoint.

**Response** `200`: `{"status": "ok"}`

---

## Response Models

### CandidateRead

```json
{
  "id": 1,
  "name": "Jane Doe",
  "email": "jane@example.com",
  "skills": ["Python", "FastAPI"],
  "experience": 5,
  "resume_url": "https://example.com/resume.pdf",
  "created_at": "2025-01-15T10:30:00"
}
```

### JobRead

```json
{
  "id": 1,
  "title": "Backend Developer",
  "description": "Build scalable APIs",
  "requirements": ["Python", "PostgreSQL", "FastAPI"],
  "location": "Remote",
  "salary_range": "$80k–$120k",
  "created_at": "2025-01-15T10:30:00"
}
```

### EvaluationRead

```json
{
  "id": 1,
  "candidate_id": 1,
  "job_id": 1,
  "status": "completed",
  "score": 85,
  "summary": "Strong match with minor gaps in cloud experience.",
  "strengths": ["Expert in Python", "FastAPI experience"],
  "weaknesses": ["Limited AWS experience"],
  "recommendations": ["Consider AWS certification"],
  "created_at": "2025-01-15T10:30:00",
  "completed_at": "2025-01-15T10:30:45"
}
```

### Evaluation Statuses

| Status | Meaning |
|--------|---------|
| `pending` | Created, waiting for background processor |
| `in_progress` | LLM analysis is running |
| `completed` | Results available (score, summary, etc.) |
| `failed` | Processing error — may be retried by re-POSTing |

---

## Error Responses

All errors follow this shape:

```json
{
  "detail": "Human-readable message",
  "error_type": "unique | foreign_key | not_null | check | database_error"
}
```

| HTTP Code | When |
|-----------|------|
| `404` | Resource not found |
| `409` | Integrity constraint violation (duplicate email, missing FK, etc.) |
| `500` | Unexpected server error |
