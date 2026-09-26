from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from ..models import Timetable, Subject


DAY_ORDER_MAP = {
    "1": "Day I", "i": "Day I", "day 1": "Day I", "day i": "Day I", "day one": "Day I", "first day": "Day I", "monday": "Day I",
    "2": "Day II", "ii": "Day II", "day 2": "Day II", "day ii": "Day II", "day two": "Day II", "second day": "Day II", "tuesday": "Day II",
    "3": "Day III", "iii": "Day III", "day 3": "Day III", "day iii": "Day III", "day three": "Day III", "third day": "Day III", "wednesday": "Day III",
    "4": "Day IV", "iv": "Day IV", "day 4": "Day IV", "day iv": "Day IV", "day four": "Day IV", "fourth day": "Day IV", "thursday": "Day IV",
    "5": "Day V", "v": "Day V", "day 5": "Day V", "day v": "Day V", "day five": "Day V", "fifth day": "Day V", "friday": "Day V",
    "6": "Day VI", "vi": "Day VI", "day 6": "Day VI", "day vi": "Day VI", "day six": "Day VI", "sixth day": "Day VI", "saturday": "Day VI",
}


def normalize_day_order(text: str) -> Optional[str]:
    """Normalizes various day order references to 'Day I' through 'Day VI'."""
    cleaned = text.strip().lower()
    if cleaned in DAY_ORDER_MAP:
        return DAY_ORDER_MAP[cleaned]
    for key, val in DAY_ORDER_MAP.items():
        if key in cleaned:
            return val
    return None


def get_all_timetable(db: Session) -> List[Timetable]:
    """Retrieves all timetable entries ordered by day and start time."""
    return db.query(Timetable).all()


def get_day_schedule(db: Session, day_order: str) -> List[Timetable]:
    """Retrieves scheduled periods for a specific day order."""
    normalized = normalize_day_order(day_order) or day_order
    return db.query(Timetable).filter(
        func.lower(Timetable.day_order) == normalized.lower()
    ).all()


def get_subject_timetable(db: Session, subject_query: str) -> List[Timetable]:
    """Finds all timetable slots for a given subject (theory or lab)."""
    sub_lower = subject_query.strip().lower()
    return db.query(Timetable).filter(
        or_(
            func.lower(Timetable.subject).contains(sub_lower),
            Timetable.subject_rel.has(func.lower(Subject.name).contains(sub_lower)),
            Timetable.subject_rel.has(func.lower(Subject.code).contains(sub_lower)),
        )
    ).all()


def get_labs(db: Session) -> List[Timetable]:
    """Retrieves all lab sessions."""
    return db.query(Timetable).filter(
        or_(
            Timetable.class_type == "Lab",
            func.lower(Timetable.subject).contains("lab")
        )
    ).all()


def get_faculty_info(db: Session, faculty_query: str) -> List[Timetable]:
    """Finds timetable entries handled by a specific faculty member."""
    fac_lower = faculty_query.strip().lower()
    return db.query(Timetable).filter(
        func.lower(Timetable.faculty).contains(fac_lower)
    ).all()


def get_room_for_subject(db: Session, subject_query: str) -> List[Dict[str, Any]]:
    """Returns rooms and times for a given subject or lab."""
    slots = get_subject_timetable(db, subject_query)
    results = []
    for s in slots:
        if s.room:
            results.append({
                "subject": s.subject,
                "room": s.room,
                "day_order": s.day_order,
                "time": f"{s.start_time} - {s.end_time}",
                "class_type": s.class_type
            })
    return results


def get_breaks_and_lunch() -> Dict[str, str]:
    """Returns standard college break and lunch timings."""
    return {
        "break": "12:00 PM - 12:15 PM",
        "lunch": "1:15 PM - 2:00 PM"
    }
