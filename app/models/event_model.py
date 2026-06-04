from sqlalchemy import String, Text, ForeignKey, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db_async import Base
from datetime import datetime
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.event_model import RSVP


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text)
    date: Mapped[str] = mapped_column(String(100))  
    location: Mapped[str] = mapped_column(String(200))
    flyer_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(server_default=func.now(), onupdate=func.now())


    #One-to-Many: event has many RSVPs
    rsvps: Mapped[list["RSVP"]] = relationship(
        "RSVP",
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


class RSVP(Base):
    __tablename__ = "rsvps"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), index=True)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    #Many-to-One: RSVP belongs to an event
    event: Mapped["Event"] = relationship("Event", back_populates="rsvps")

    #A given email can only RSVP once per event
    __table_args__ = (
        UniqueConstraint("event_id", "email", name="uq_rsvp_event_email"),
    )