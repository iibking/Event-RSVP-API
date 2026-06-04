from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app.models.event_model import Event
from app.schemas.event_schema import EventCreate, EventUpdate


class EventRepository:

    @staticmethod
    async def get_by_id(db: AsyncSession, event_id: int) -> Event | None:
        result = await db.execute(
            select(Event)
            .where(Event.id == event_id)
            .options(selectinload(Event.rsvps))
        )
        return result.scalars().first()

    @staticmethod
    async def get_all_paginated(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20,
        search: str | None = None,
    ) -> tuple[list[Event], int]:
        stmt = select(Event).options(selectinload(Event.rsvps))

        if search:
            stmt = stmt.where(Event.title.ilike(f"%{search}%"))

        # Count total (for pagination metadata)
        count_result = await db.execute(
            select(func.count()).select_from(stmt.subquery())
        )
        total = count_result.scalar()

        stmt = stmt.order_by(Event.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        events = result.scalars().all()
        return events, total

    @staticmethod
    async def create(db: AsyncSession, data: EventCreate) -> Event:
        event = Event(**data.model_dump())
        db.add(event)
        await db.flush()
        await db.refresh(event)
        return event

    @staticmethod
    async def update(db: AsyncSession, event: Event, data: EventUpdate) -> Event:
        fields = data.model_dump(exclude_unset=True)
        for key, value in fields.items():
            setattr(event, key, value)
        await db.flush()
        await db.refresh(event)
        return event

    @staticmethod
    async def delete(db: AsyncSession, event: Event) -> None:
        # cascade="all, delete-orphan" removes related RSVPs automatically.
        await db.delete(event)
        await db.flush()