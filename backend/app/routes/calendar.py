from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import CalendarEventResponse
from ..services.calendar_service import (
    get_all_events,
    get_events_by_date,
    get_events_by_month,
    get_holidays,
    get_working_days,
)

router = APIRouter(prefix="/api/calendar", tags=["Calendar"])


@router.get("", response_model=List[CalendarEventResponse])
def get_calendar_events(
    category: Optional[str] = Query(None, description="Filter by event category"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
    is_holiday: Optional[bool] = Query(None, description="Filter holidays"),
    db: Session = Depends(get_db),
):
    """Retrieves all academic calendar events with optional filters."""
    return get_all_events(db, category=category, semester=semester, is_holiday=is_holiday)


@router.get("/holidays", response_model=List[CalendarEventResponse])
def get_calendar_holidays(
    month: Optional[str] = Query(None, description="Optional month name or number"),
    db: Session = Depends(get_db),
):
    """Retrieves all officially declared holidays."""
    return get_holidays(db, month_query=month)


@router.get("/date/{date}", response_model=List[CalendarEventResponse])
def get_events_for_date(date: str, db: Session = Depends(get_db)):
    """Retrieves events for a specific date (YYYY-MM-DD or partial match)."""
    events = get_events_by_date(db, date)
    if not events:
        raise HTTPException(status_code=404, detail=f"No academic calendar events found for {date}")
    return events


@router.get("/month/{month}", response_model=List[CalendarEventResponse])
def get_events_for_month(month: str, db: Session = Depends(get_db)):
    """Retrieves all academic events for a given month."""
    events = get_events_by_month(db, month)
    if not events:
        raise HTTPException(status_code=404, detail=f"No calendar events found for month {month}")
    return events


@router.get("/working-days")
def get_working_days_endpoint(month: Optional[str] = Query(None)):
    """Retrieves working day totals from PSGCAS academic calendar."""
    return get_working_days(month)
