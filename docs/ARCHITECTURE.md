# Proposed Architecture

This architecture is a starting proposal. The bootstrap ExecPlan must validate it before code scaffolding.

## Guiding choice

Use a small modular monolith plus a native Android client. This keeps operations simple while preserving clean seams for AI providers, catalog sources, pricing sources, storage, and future training jobs.

```text
Android app ─┐
             ├── HTTPS JSON/multipart API ── FastAPI application ── PostgreSQL/pgvector
Web app ─────┘                                  │
                                                ├── Local filesystem BlobStore
                                                ├── OpenAI adapter
                                                ├── Gemini adapter
                                                ├── LEGO catalog adapters
                                                └── Pricing adapters
```

## Proposed stack

### `apps/web`

- TypeScript
- React with Next.js
- Responsive, mobile-friendly appraisal/history interface
- Generated or schema-derived API client

### `apps/android`

- Kotlin
- Jetpack Compose
- Android Share Target
- AccessibilityService/overlay capture spike for supported devices
- Secure upload client

### `services/api`

- Python
- FastAPI
- Pydantic schemas
- SQLAlchemy and Alembic
- Pillow/OpenCV only where needed for image processing
- Provider adapters and deterministic valuation engine

### Data and storage

- PostgreSQL for records and relationships
- pgvector when reference-image and query embeddings are introduced
- Local filesystem behind a `BlobStore` interface for MVP
- SHA-256 content addressing and exact deduplication
- Future S3/MinIO adapter without changing domain logic

### Development/deployment

- Docker Compose for local dependencies and eventual single-host deployment
- `pnpm` for web packages
- `uv` for Python dependency/environment management
- Gradle for Android
- No queue/broker initially; introduce a worker only after processing latency or reliability demonstrates the need

## Core server modules

```text
services/api/app/
  api/              HTTP routes and request/response schemas
  domain/           Entities, enums, and business rules
  application/      Use cases/orchestration
  persistence/      SQLAlchemy models and repositories
  storage/          BlobStore interface and filesystem implementation
  images/           Metadata, hashing, derivatives, crops, dedupe
  recognition/      Candidate generation, ranking, verification
  catalog/          Rebrickable/BrickLink/local catalog adapters
  pricing/          Price sources, snapshots, normalization
  valuation/        Transparent calculations and offer rules
  providers/        OpenAI/Gemini clients, cost/usage logging
  datasets/         Label state and export/versioning
```

## Recognition pipeline target

1. Validate and normalize the listing images.
2. Extract text clues such as visible set numbers, box text, title, and description.
3. Detect/crop likely LEGO objects when needed.
4. Embed listing image/object crop.
5. Retrieve top catalog reference matches with vector similarity.
6. Merge vector matches with text/catalog matches.
7. Send only the strongest candidates and evidence to a multimodal verifier.
8. Return ranked candidates, contradictions, confidence, and missing-view requests.
9. Persist the complete run with provider/model/prompt versions.
10. Accept Brian's correction as a separate confirmation event.

## Storage design

Originals are immutable. A single physical blob may be referenced by several records, but every transformation is a new asset with lineage:

```text
raw_screen_capture
  └── listing_photo_crop
        ├── thumbnail
        ├── normalized_analysis_image
        └── object_crop
              └── training_derivative
```

Use database records, not directory names, as the source of truth.

## API direction

Start with a small API:

- `POST /listings`
- `GET /listings`
- `GET /listings/{id}`
- `PATCH /listings/{id}`
- `POST /listings/{id}/images`
- `GET /images/{id}/content` or controlled signed/streamed access
- `POST /listings/{id}/analysis-runs`
- `GET /analysis-runs/{id}`
- `POST /candidate-matches/{id}/confirm`

Do not lock the exact route shapes until the foundation plan is reviewed.

## Architecture decisions intentionally deferred

- Exact stable framework/library versions
- Whether the web app is separately deployed or served behind one reverse proxy
- Background-job technology
- S3/MinIO adoption
- Remote authentication mechanism
- Exact catalog/pricing provider combination
- Production AI model choices
- Custom model training framework
