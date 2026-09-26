from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import TimetableResponse
from ..services.timetable_service import (
    get_all_timetable,
    get_day_schedule,
    get_subject_timetable,
    normalize_day_order,
)

router = APIRouter(prefix="/api/timetable", tags=["Timetable"])


@router.get("", response_model=List[TimetableResponse])
def get_full_timetable(db: Session = Depends(get_db)):
    """Retrieves all timetable periods for MCA Semester III."""
    return get_all_timetable(db)


@router.get("/day/{day_order}", response_model=List[TimetableResponse])
def get_schedule_by_day(day_order: str, db: Session = Depends(get_db)):
    """Retrieves schedule for a specific day order (e.g. Day I, Day II)."""
    norm_day = normalize_day_order(day_order)
    if not norm_day:
        norm_day = day_order
    schedule = get_day_schedule(db, norm_day)
    if not schedule:
        raise HTTPException(status_code=404, detail=f"No timetable found for day {day_order}")
    return schedule


@router.get("/subject/{subject}", response_model=List[TimetableResponse])
def get_schedule_by_subject(subject: str, db: Session = Depends(get_db)):
    """Retrieves timetable slots for a specific subject."""
    slots = get_subject_timetable(db, subject)
    if not slots:
        raise HTTPException(status_code=404, detail=f"No schedule found for subject {subject}")
    return slots
