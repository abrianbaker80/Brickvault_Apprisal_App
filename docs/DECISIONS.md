# Project Decisions

This file records durable decisions. Codex should update it when an accepted plan changes one.

## Accepted

### D-001 — Private single-user product

The application is built solely for Brian. No public registration, billing, team roles, or app-store distribution is required.

### D-002 — Self-hosted source of truth

Images, labels, appraisals, and provider credentials will be controlled by Brian's server. Clients call the server rather than external providers directly.

### D-003 — Save training-useful data from the beginning

The MVP must preserve immutable originals, useful crops, prediction history, and Brian's corrections. Dataset labeling is part of the product, not an afterthought.

### D-004 — Human confirmation separates prediction from truth

An AI result cannot automatically become a verified training label.

### D-005 — Retrieval and verification precede custom training

Index reference images and metadata, retrieve candidates, and use multimodal verification before investing in a custom model.

### D-006 — Explicit user-triggered Facebook capture only

Do not scrape, intercept, or autonomously navigate Facebook. Brian triggers each capture/session.

### D-007 — Keep ordinary uploads and Android Share as fallbacks

The app must remain usable when the overlay/accessibility path breaks or Facebook changes its UI.

### D-008 — Risk-first development

Prove the image-storage path, Android capture feasibility, and recognition quality in isolated milestones before building the complete workflow.

## Proposed; validate during bootstrap

### P-001 — Modular-monolith backend in Python/FastAPI

Chosen for image/ML ecosystem and a simple self-hosted deployment.

### P-002 — Next.js/TypeScript browser UI

Chosen for a modern responsive interface and broad ecosystem support.

### P-003 — Native Kotlin/Jetpack Compose Android client

Required for Share Target, AccessibilityService, overlay, and supported screen-capture APIs.

### P-004 — PostgreSQL plus pgvector

Use PostgreSQL from the beginning for durable metadata; add pgvector when visual retrieval is implemented.

### P-005 — Local filesystem blobs behind an abstraction for MVP

Avoid running MinIO initially. Preserve the ability to add S3-compatible storage later.
