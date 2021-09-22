from typing import Optional, List
from uuid import uuid4

import redis
from fastapi import FastAPI, HTTPException
from collections import namedtuple
from pydantic import BaseModel
from tinydb import TinyDB, Query

# app & redis
app = FastAPI()
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# event storage
event_storage = TinyDB("./event_storage.json")
EventQuery = Query()

# custom errors
Error = namedtuple("Error", "response_model exception")
EVENT_ID_CONFLICT = Error(response_model={"description": "Conflict - Event ID already in use", "model": str},
                          exception=HTTPException(409, "Event id is already used. Change the event id or omit it, "
                                                       "then a random uuid will be used"))

# models
class Event(BaseModel):
    type: str
    id: Optional[str] = None
    time: Optional[str] = None
    description: Optional[str] = None
    payload: dict


class EventId(BaseModel):
    id: str


@app.post("/{id}", response_model=EventId, responses={409: EVENT_ID_CONFLICT.response_model})
async def add_event(id: str, e: Event):
    # check event id (if not specified, generate uuid for the event)
    if e.id and event_storage.contains(EventQuery.id == e.id):
        raise EVENT_ID_CONFLICT.exception
    else:
        e.id = str(uuid4())

    # store event in storage and add id to events list of given id
    event_storage.insert(e.dict())
    r.rpush(f"{id}:events", e.id)

    # return event id
    return EventId(id=e.id)


@app.get("/{id}", response_model=List[Event])
async def get_events(id: str):
    # retrieve cursor (points at the oldest unread event)
    cursor = r.get(f"{id}:cursor")
    cursor = 0 if cursor is None else cursor

    # retrieve event ids from event list
    event_ids = r.lrange(f"{id}:events", cursor, -1)
    print(event_ids)

    # retrieve event for each event id
    events = event_storage.search(EventQuery.id.one_of(event_ids))

    # update cursor
    r.incr(f"{id}:cursor", len(events))

    # return events
    return events
