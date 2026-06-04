from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.event_model import RSVP
from app.schemas.event_schema import RSVPCreate


class RsvpRepository:

    @staticmethod
    async def get_by_event(db: AsyncSession, event_id: int) -> list[RSVP]:
        result = await db.execute(
            select(RSVP)
            .where(RSVP.event_id == event_id)
            .order_by(RSVP.created_at.asc())
        )
        return result.scalars().all()

    @staticmethod
    async def get_by_event_and_email(
        db: AsyncSession, event_id: int, email: str
    ) -> RSVP | None:
        result = await db.execute(
            select(RSVP).where(RSVP.event_id == event_id, RSVP.email == email)
        )
        return result.scalars().first()

    @staticmethod
    async def create(db: AsyncSession, data: RSVPCreate, event_id: int) -> RSVP:
        rsvp = RSVP(name=data.name, email=data.email, event_id=event_id)
        db.add(rsvp)
        await db.flush()
        await db.refresh(rsvp)
        return rsvp