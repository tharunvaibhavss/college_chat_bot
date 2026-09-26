from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# -------------------------------------------------------------
# Chat Schemas
# -------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str = Field(..., description="Student's natural-language question")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Chatbot answer")
    intent: str = Field(..., description="Identified NLP intent")
    sources: List[str] = Field(default_factory=list, description="Authoritative data sources")


# -------------------------------------------------------------
# Timetable Schemas
# -------------------------------------------------------------
class TimetableBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    day_order: str
    start_time: str
    end_time: str
    subject: str
    room: Optional[str] = None
    faculty: Optional[str] = None
    class_type: str


class TimetableResponse(TimetableBase):
    id: int
    subject_id: Optional[int] = None


class DayScheduleResponse(BaseModel):
    day_order: str
    periods: List[TimetableResponse]


# -------------------------------------------------------------
# Subject Schemas
# -------------------------------------------------------------
class SubjectBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    description: Optional[str] = None
    class_type: str
    faculty: Optional[str] = None


class SubjectResponse(SubjectBase):
    id: int


class SubjectScheduleSlot(BaseModel):
    day_order: str
    start_time: str
    end_time: str
    room: Optional[str] = None
    faculty: Optional[str] = None
    class_type: str


class SubjectDetailResponse(SubjectResponse):
    schedules: List[SubjectScheduleSlot] = []


# -------------------------------------------------------------
# Calendar Event Schemas
# -------------------------------------------------------------
class CalendarEventBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    date: str
    day: str
    event: str
    category: str
    semester: Optional[str] = None
    is_holiday: bool = False
    description: Optional[str] = None


class CalendarEventResponse(CalendarEventBase):
    id: int


# -------------------------------------------------------------
# Health Schema
# -------------------------------------------------------------
class HealthResponse(BaseModel):
    status: str
    message: str
    version: str
