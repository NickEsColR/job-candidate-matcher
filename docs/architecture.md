---
title: Architecture
---

# Architecture

Job-Candidate-Matcher is structured around three core modules that work together to provide AI-powered candidate evaluation capabilities.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Layer                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐│
│  │  Candidates  │  │    Jobs     │  │     Evaluations         ││
│  │   Router     │  │   Router    │  │      Router             ││
│  └─────────────┘  └─────────────┘  └─────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Core Module                            │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │   Pydantic Models    │  │      SQLModel Entities          │ │
│  │   (Request/Response) │  │      (Database Tables)          │ │
│  └──────────────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent Engine Module                           │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │   OpenAI Client      │  │     Agent Loop (Reasoning)       │ │
│  │   (Function Calls)   │  │     - Analyze Requirements      │ │
│  └──────────────────────┘  │     - Evaluate Skills           │ │
│                            │     - Generate Scores             │ │
│                            │     - Produce Recommendations     │ │
│                            └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     Quality Module                               │
│  ┌──────────────────────┐  ┌──────────────────────────────────┐ │
│  │   Evaluation Logs   │  │      Tool Execution Logs         │ │
│  │   (Audit Trail)     │  │      (Debugging/Tracing)         │ │
│  └──────────────────────┘  └──────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│   candidates    │       │      jobs       │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ name            │       │ title           │
│ email           │       │ description     │
│ skills          │       │ requirements    │
│ experience      │       │ location        │
│ resume_url      │       │ salary_range    │
│ created_at      │       │ created_at      │
└─────────────────┘       └─────────────────┘
         │                        │
         │                        │
         ▼                        ▼
┌─────────────────────────────────────────────┐
│              evaluations                    │
├─────────────────────────────────────────────┤
│ id (PK)                                      │
│ candidate_id (FK)                          │
│ job_id (FK)                                 │
│ status (pending/processing/completed/failed│
│ score (0-100)                               │
│ summary                                     │
│ strengths (JSON array)                     │
│ weaknesses (JSON array)                    │
│ recommendations (JSON array)                │
│ created_at                                  │
│ completed_at                                │
└─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│               tool_logs                     │
├─────────────────────────────────────────────┤
│ id (PK)                                      │
│ evaluation_id (FK)                          │
│ tool_name                                   │
│ input_data (JSON)                          │
│ output_data (JSON)                         │
│ created_at                                  │
└─────────────────────────────────────────────┘
```
