# Event RSVP System

A database-backed REST API for creating events and managing RSVPs, built with
FastAPI and an async SQLAlchemy stack on PostgreSQL. Originally an in-memory
prototype, it was rebuilt into a clean, layered, migration-managed service.

## Features
- Create, read, update, and delete events
- Optional event flyer upload
- RSVP to an event (with duplicate-RSVP protection)
- List RSVPs for an event
- Paginated, searchable event listing
- Fully async database access
- Schema managed by Alembic migrations

## Tech stack
- **FastAPI** – web framework
- **SQLAlchemy 2.0 (async)** + **asyncpg** – ORM / database driver
- **PostgreSQL** – database
- **Alembic** – schema migrations
- **Pydantic v2 / pydantic-settings** – validation & configuration
- **Uvicorn** – ASGI server

## Architecture
Layered separation of concerns:

    API router  ->  Service (business logic)  ->  Repository (DB access)  ->  Model

## Project structure
    Event-RSVP-System-V1/
    ├── .env.example              # template for environment variables
    ├── alembic.ini               # Alembic configuration
    ├── requirements.txt
    ├── README.md
    ├── alembic/
    │   ├── env.py                # migration environment (points at Base.metadata)
    │   ├── script.py.mako
    │   └── versions/             # migration files
    └── app/
        ├── main.py               # FastAPI app + router registration
        ├── core/
        │   ├── config.py         # settings (env-driven)
        │   ├── db_async.py       # async engine + Base (used by the app)
        │   ├── db.py             # sync engine (used by Alembic)
        │   └── deps.py           # get_async_db dependency
        ├── models/
        │   └── event_model.py    # Event and RSVP ORM models
        ├── schemas/
        │   └── event_schema.py   # Pydantic request/response models
        ├── repositories/
        │   ├── event_repository.py
        │   └── rsvp_repository.py
        ├── services/
        │   └── event_service.py
        └── api/v1/
            └── event.py          # /events routes

## Prerequisites
- Python 3.10+
- A running PostgreSQL instance

## Setup
1. Clone the repository and enter it:
```bash
   git clone https://github.com/iibking/Event-RSVP-System-V1.git
   cd Event-RSVP-System-V1
```
2. Create and activate a virtual environment:
```bash
   python -m venv venv
   venv\Scripts\activate          # Windows
   # source venv/bin/activate     # macOS/Linux
```
3. Install dependencies:
```bash
   pip install -r requirements.txt
```
4. Create the PostgreSQL database:
```bash
   createdb event_rsvp
```
5. Create your environment file from the template and fill it in:
```bash
   cp .env.example .env
```

## Environment variables
| Variable             | Description                                   | Example                                                          |
|----------------------|-----------------------------------------------|------------------------------------------------------------------|
| `DATABASE_URL`       | Sync URL — used by Alembic                     | `postgresql://postgres:pass@localhost:5432/event_rsvp`           |
| `DATABASE_URL_ASYNC` | Async URL — used by the app (asyncpg driver)   | `postgresql+asyncpg://postgres:pass@localhost:5432/event_rsvp`   |
| `ENVIRONMENT`        | `DEBUG` enables SQL echo                       | `DEBUG`                                                          |

Both database URLs must point at the **same** database, differing only in the
driver (`postgresql://` vs `postgresql+asyncpg://`).

## Running migrations
Alembic manages the schema. Apply the existing migrations:
```bash
alembic upgrade head
```
To create a new migration after changing a model (use double quotes on Windows):
```bash
alembic revision --autogenerate -m "describe your change"
alembic upgrade head
```
Check the current revision:
```bash
alembic current
```

## Running the app
From the project root:
```bash
uvicorn app.main:app --reload
```
Interactive API docs: http://127.0.0.1:8000/docs

## API endpoints
| Method | Path                          | Description                                  |
|--------|-------------------------------|----------------------------------------------|
| GET    | `/events/`                    | List events (paginated; `skip`, `limit`, `search`) |
| POST   | `/events/`                    | Create an event (multipart form; optional flyer) |
| GET    | `/events/{event_id}`          | Retrieve a single event (with its RSVPs)     |
| PATCH  | `/events/{event_id}`          | Update an event                              |
| DELETE | `/events/{event_id}`          | Delete an event (and its RSVPs)              |
| POST   | `/events/{event_id}/rsvp`     | RSVP to an event (form: `name`, `email`)     |
| GET    | `/events/{event_id}/rsvps`    | List RSVPs for an event                      |

## Business rules
- An event must exist before it can be retrieved, updated, or RSVP'd to (`404` otherwise).
- A given email can RSVP to a given event only once — enforced by a unique
  constraint on `(event_id, email)`; a duplicate returns `400`.
- Deleting an event cascades to its RSVPs.