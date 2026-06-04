from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


#RSVP
class RSVPCreate(BaseModel):
    name: str
    email: str


class RSVPRead(BaseModel):
    id: int
    name: str
    email: str
    event_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


#Event
class EventCreate(BaseModel):
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    date: Optional[str] = None
    location: Optional[str] = None
    flyer_filename: Optional[str] = None


class EventRead(BaseModel):
    id: int
    title: str
    description: str
    date: str
    location: str
    flyer_filename: Optional[str] = None
    created_at: datetime
    rsvps: list[RSVPRead] = []

    model_config = ConfigDict(from_attributes=True)


class PaginatedEvents(BaseModel):
    items: list[EventRead]
    total: int
    skip: int
    limit: int



