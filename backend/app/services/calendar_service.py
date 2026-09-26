from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from ..models import CalendarEvent

MONTH_MAP = {
    "january": "01", "jan": "01", "1": "01", "01": "01",
    "february": "02", "feb": "02", "2": "02", "02": "02",
    "march": "03", "mar": "03", "3": "03", "03": "03",
    "april": "04", "apr": "04", "4": "04", "04": "04",
    "may": "05", "may": "05", "5": "05", "05": "05",
    "june": "06", "jun": "06", "6": "06", "06": "06",
    "july": "07", "jul": "07", "7": "07", "07": "07",
    "august": "08", "aug": "08", "8": "08", "08": "08",
    "september": "09", "sep": "09", "sept": "09", "9": "09", "09": "09",
    "october": "10", "oct": "10", "10": "10",
    "november": "11", "nov": "11", "11": "11",
    "december": "12", "dec": "12", "12": "12"
}

MONTH_NAMES = {
    "01": "January", "02": "February", "03": "March", "04": "April",
    "05": "May", "06": "June", "07": "July", "08": "August",
    "09": "September", "10": "October", "11": "November", "12": "December"
}

# Official working day totals from PSGCAS Handbook / Calendar
MONTHLY_WORKING_DAYS = {
    "01": 18,  # January
    "02": 20,  # February
    "03": 21,  # March
    "04": 10,  # April
    "06": 12,  # June (Odd sem start June 15)
    "07": 23,  # July
    "08": 21,  # August
    "09": 21,  # September
    "10": 15,  # October (Last working day Oct 23)
    "12": 21,  # December
}


def normalize_month(query: str) -> Optional[str]:
    """Returns two-digit month string '01'-'12' or None."""
    q = query.strip().lower()
    return MONTH_MAP.get(q)


def get_all_events(
    db: Session,
    category: Optional[str] = None,
    semester: Optional[str] = None,
    is_holiday: Optional[bool] = None
) -> List[CalendarEvent]:
    query = db.query(CalendarEvent)
    if category:
        query = query.filter(func.lower(CalendarEvent.category) == category.lower())
    if semester:
        query = query.filter(func.lower(CalendarEvent.semester) == semester.lower())
    if is_holiday is not None:
        query = query.filter(CalendarEvent.is_holiday == is_holiday)
    return query.order_by(CalendarEvent.date.asc()).all()


def get_events_by_date(db: Session, date_str: str) -> List[CalendarEvent]:
    """Retrieves calendar events matching a specific date or partial date."""
    clean = date_str.strip()
    return db.query(CalendarEvent).filter(
        or_(
            CalendarEvent.date == clean,
            CalendarEvent.date.contains(clean),
            func.lower(CalendarEvent.event).contains(clean.lower())
        )
    ).all()


def get_events_by_month(db: Session, month_query: str) -> List[CalendarEvent]:
    """Retrieves all calendar events in a given month."""
    m_num = normalize_month(month_query)
    if not m_num:
        # Try checking if month name appears in string
        for m_name, code in MONTH_MAP.items():
            if m_name in month_query.lower():
                m_num = code
                break
    if not m_num:
        return []
    # Match pattern -MM-
    pattern = f"-{m_num}-"
    return db.query(CalendarEvent).filter(CalendarEvent.date.contains(pattern)).order_by(CalendarEvent.date.asc()).all()


def get_holidays(db: Session, month_query: Optional[str] = None) -> List[CalendarEvent]:
    """Retrieves holidays optionally filtered by month."""
    query = db.query(CalendarEvent).filter(CalendarEvent.is_holiday == True)
    if month_query:
        m_num = normalize_month(month_query)
        if m_num:
            query = query.filter(CalendarEvent.date.contains(f"-{m_num}-"))
    return query.order_by(CalendarEvent.date.asc()).all()


def get_ca_tests(db: Session, test_identifier: Optional[str] = None) -> List[CalendarEvent]:
    """Retrieves CA test dates (I CA or II CA)."""
    query = db.query(CalendarEvent).filter(CalendarEvent.category == "CA Test")
    if test_identifier:
        t_clean = test_identifier.strip().upper()
        if "I CA" in t_clean and "II" not in t_clean and "2" not in t_clean:
            query = query.filter(
                CalendarEvent.event.contains("I CA"),
                ~CalendarEvent.event.contains("II CA")
            )
        elif "II CA" in t_clean or "2" in t_clean:
            query = query.filter(CalendarEvent.event.contains("II CA"))
    return query.order_by(CalendarEvent.date.asc()).all()


def get_fee_deadlines(db: Session, semester: Optional[str] = None) -> List[CalendarEvent]:
    """Retrieves examination fee payment schedules and deadlines."""
    query = db.query(CalendarEvent).filter(CalendarEvent.category == "Fee Payment")
    if semester:
        query = query.filter(func.lower(CalendarEvent.semester) == semester.lower())
    return query.order_by(CalendarEvent.date.asc()).all()


def get_semester_milestones(db: Session, semester: Optional[str] = None) -> List[CalendarEvent]:
    """Retrieves commencement and last working day events."""
    query = db.query(CalendarEvent).filter(
        or_(
            CalendarEvent.category == "Semester Date",
            CalendarEvent.category == "Examination"
        )
    )
    if semester:
        query = query.filter(func.lower(CalendarEvent.semester).contains(semester.lower()))
    return query.order_by(CalendarEvent.date.asc()).all()


def get_working_days(month_query: Optional[str] = None) -> Dict[str, Any]:
    """Returns monthly working-day totals from the PSGCAS academic calendar."""
    if month_query:
        m_num = normalize_month(month_query)
        if m_num and m_num in MONTHLY_WORKING_DAYS:
            return {
                "month": MONTH_NAMES.get(m_num, month_query),
                "working_days": MONTHLY_WORKING_DAYS[m_num]
            }
    return {
        "monthly_totals": {
            MONTH_NAMES[k]: v for k, v in MONTHLY_WORKING_DAYS.items()
        }
    }
