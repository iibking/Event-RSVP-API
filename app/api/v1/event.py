from typing import Optional
from fastapi import APIRouter, Depends, File, Form, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.deps import get_async_db
from app.services.event_service import EventService
from app.schemas.event_schema import (
    EventCreate,
    EventUpdate,
    EventRead,
    RSVPCreate,
    RSVPRead,
    PaginatedEvents,
)


router = APIRouter(prefix="/events", tags=["Events"])


# GET /events/ - List all events (paginated)
@router.get("/", response_model=PaginatedEvents)
async def list_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_async_db),
):
    return await EventService.get_events(db, skip=skip, limit=limit, search=search)


# POST /events/ - Create a new event
@router.post("/", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    location: str = Form(...),
    flyer: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_async_db),
):
    data = EventCreate(
        title=title,
        description=description,
        date=date,
        location=location,
        flyer_filename=flyer.filename if flyer else None,
    )
    event = await EventService.create_event(db, data)
    await db.commit()
    return event


# GET /events/{event_id} - Get event by id
@router.get("/{event_id}", response_model=EventRead)
async def get_event(event_id: int, db: AsyncSession = Depends(get_async_db)):
    return await EventService.get_event(db, event_id)


# PATCH /events/{event_id} - Update an event
@router.patch("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: int,
    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    date: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    flyer: Optional[UploadFile] = File(None),
    db: AsyncSession = Depends(get_async_db),
):
    # Only include fields the client actually sent, so a partial PATCH
    # doesn't overwrite untouched columns with None.
    provided = {
        "title": title,
        "description": description,
        "date": date,
        "location": location,
    }
    provided = {k: v for k, v in provided.items() if v is not None}
    if flyer:
        provided["flyer_filename"] = flyer.filename

    data = EventUpdate(**provided)
    event = await EventService.update_event(db, event_id, data)
    await db.commit()
    return event


# DELETE /events/{event_id} - Remove an event and its RSVPs
@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(event_id: int, db: AsyncSession = Depends(get_async_db)):
    await EventService.delete_event(db, event_id)
    await db.commit()


# POST /events/{event_id}/rsvp - RSVP to an event
@router.post(
    "/{event_id}/rsvp",
    response_model=RSVPRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_rsvp(
    event_id: int,
    name: str = Form(...),
    email: str = Form(...),
    db: AsyncSession = Depends(get_async_db),
):
    data = RSVPCreate(name=name, email=email)
    rsvp = await EventService.create_rsvp(db, event_id, data)
    await db.commit()
    return rsvp


# GET /events/{event_id}/rsvps - List RSVPs for an event
@router.get("/{event_id}/rsvps", response_model=list[RSVPRead])
async def get_event_rsvps(event_id: int, db: AsyncSession = Depends(get_async_db)):
    return await EventService.get_event_rsvps(db, event_id)