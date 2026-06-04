from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event_model import Event, RSVP
from app.repositories.event_repository import EventRepository
from app.repositories.rsvp_repository import RsvpRepository
from app.schemas.event_schema import (
    EventCreate,
    EventUpdate,
    RSVPCreate,
    PaginatedEvents,
)


class EventService:

    # Events
    @staticmethod
    async def create_event(db: AsyncSession, data: EventCreate) -> Event:
        return await EventRepository.create(db, data)

    @staticmethod
    async def get_events(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> PaginatedEvents:
        events, total = await EventRepository.get_all_paginated(db, skip, limit, search)
        return PaginatedEvents(items=events, total=total, skip=skip, limit=limit)

    @staticmethod
    async def get_event(db: AsyncSession, event_id: int) -> Event:
        event = await EventRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    @staticmethod
    async def update_event(
        db: AsyncSession, event_id: int, data: EventUpdate
    ) -> Event:
        event = await EventRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return await EventRepository.update(db, event, data)

    @staticmethod
    async def delete_event(db: AsyncSession, event_id: int) -> None:
        event = await EventRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        await EventRepository.delete(db, event)

    # RSVPs
    @staticmethod
    async def create_rsvp(
        db: AsyncSession, event_id: int, data: RSVPCreate
    ) -> RSVP:
        event = await EventRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        existing = await RsvpRepository.get_by_event_and_email(db, event_id, data.email)
        if existing:
            raise HTTPException(status_code=400, detail="Already RSVPed")

        return await RsvpRepository.create(db, data, event_id)

    @staticmethod
    async def get_event_rsvps(db: AsyncSession, event_id: int) -> list[RSVP]:
        event = await EventRepository.get_by_id(db, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return await RsvpRepository.get_by_event(db, event_id)