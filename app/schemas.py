from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import date


# this is "data" class for the type of events
class EventType(Enum):
    # to-do: alls no puede ser parte de esta clase porque permite crear eventos de tipo all
    # Lo hice para poder usar lista en swagger al seleccionar el tipo de evento
    commercial = "commercial"
    service = "service"
    online_meeting = "online_meeting"
    other = "other"
    alls = "all"


class EventCreate(BaseModel):
    name: str
    type: EventType
    description: str
    event_date: date


class Event(EventCreate):
    id: int
    checked: bool
    work: bool | None

    class Config:
        orm_mode = True


class EventEdit(BaseModel):
    name: str | None = None
    type: str | None = None
    description: str | None = None
    event_date: date | None = None
    checked: bool | None = None




