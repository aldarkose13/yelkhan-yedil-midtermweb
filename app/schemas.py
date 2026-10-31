from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CriminalOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: Optional[str]
    nickname: str
    reward: float
    latitude: Optional[float]
    longitude: Optional[float]
    last_known_location_note: Optional[str]
    difficulty: int
    armed: bool
    has_crew: bool
    escape_master: bool


class HuntCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")  # rejects client-sent created_at/id

    criminal_id: int
    success: bool
    notes: Optional[str] = Field(default=None, max_length=5000)


class HuntUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")  # only success / notes are editable

    success: Optional[bool] = None
    notes: Optional[str] = Field(default=None, max_length=5000)


class HuntOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    criminal_id: int
    success: bool
    notes: Optional[str]
    created_at: datetime
