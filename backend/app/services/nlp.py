import re
from typing import Dict, Any, Optional, List
from .timetable_service import normalize_day_order
from .calendar_service import MONTH_MAP


# Subject alias mappings to standard keys
SUBJECT_ALIASES = {
    "ai": "AI",
    "artificial intelligence": "AI",
    "ai lab": "AI Lab",
    "artificial intelligence lab": "AI Lab",
    "ml": "ML",
    "machine learning": "ML",
    "ml lab": "ML Lab",
    "machine learning lab": "ML Lab",
    "fsd": "FSD",
    "full stack": "FSD",
    "fullstack": "FSD",
    "full stack development": "FSD",
    "fsd lab": "FSD Lab",
    "full stack development lab": "FSD Lab",
    "am": "AM/SQA",
    "sqa": "AM/SQA",
    "am/sqa": "AM/SQA",
    "am / sqa": "AM/SQA",
    "amsqa": "AM/SQA",
    "agile": "AM/SQA",
    "agile methodologies": "AM/SQA",
    "software quality assurance": "AM/SQA",
    "tdc": "TDC (PG)",
    "tdc (pg)": "TDC (PG)",
    "tdc lab": "TDC Lab - PG",
    "tdc lab - pg": "TDC Lab - PG",
    "trans-disciplinary": "TDC (PG)",
    "technical discussion": "TDC (PG)",
}


def clean_text(text: str) -> str:
    """Preprocesses input query for NLP pipeline."""
    t = text.lower().strip()
    # Normalize question marks and trailing punctuation
    t = re.sub(r"[?!.,;]+", " ", t)
    # Collapse multiple whitespaces
    t = re.sub(r"\s+", " ", t)
    return t


def extract_entities(text: str) -> Dict[str, Any]:
    """Extracts day_order, subject, date, month, time, room, semester, etc."""
    cleaned = clean_text(text)
    entities: Dict[str, Any] = {
        "day_order": None,
        "subject": None,
        "date": None,
        "month": None,
        "time": None,
        "room": None,
        "faculty": None,
        "semester": None,
        "ca_test": None,
        "is_lab": False,
        "time_of_day": None,  # morning, afternoon
    }

    # 1. Day Order extraction
    # Patterns: Day 1, Day I, Day one, first day, on day 3, on III, Day 3
    day_match = re.search(r"\bday\s*(1|2|3|4|5|6|i{1,3}|iv|v|vi|one|two|three|four|five|six)\b", cleaned)
    if day_match:
        entities["day_order"] = normalize_day_order(day_match.group(0))
    elif re.search(r"\b(first|1st)\s+day\b", cleaned):
        entities["day_order"] = "Day I"
    elif re.search(r"\b(second|2nd)\s+day\b", cleaned):
        entities["day_order"] = "Day II"
    elif re.search(r"\b(third|3rd)\s+day\b", cleaned):
        entities["day_order"] = "Day III"
    elif re.search(r"\b(fourth|4th)\s+day\b", cleaned):
        entities["day_order"] = "Day IV"
    elif re.search(r"\b(fifth|5th)\s+day\b", cleaned):
        entities["day_order"] = "Day V"
    elif re.search(r"\b(sixth|6th)\s+day\b", cleaned):
        entities["day_order"] = "Day VI"
    elif re.search(r"\bon\s+(i{1,3}|iv|v|vi)\b", cleaned):
        raw_num = re.search(r"\bon\s+(i{1,3}|iv|v|vi)\b", cleaned).group(1)
        entities["day_order"] = normalize_day_order(raw_num)

    # 2. Subject extraction
    # Check labs explicitly first
    if "ai lab" in cleaned:
        entities["subject"] = "AI Lab"
        entities["is_lab"] = True
    elif "ml lab" in cleaned:
        entities["subject"] = "ML Lab"
        entities["is_lab"] = True
    elif "fsd lab" in cleaned:
        entities["subject"] = "FSD Lab"
        entities["is_lab"] = True
    elif "tdc lab" in cleaned:
        entities["subject"] = "TDC Lab - PG"
        entities["is_lab"] = True
    else:
        # Check longer alias matches first
        sorted_aliases = sorted(SUBJECT_ALIASES.keys(), key=lambda k: len(k), reverse=True)
        for alias in sorted_aliases:
            pattern = r"\b" + re.escape(alias) + r"\b"
            if re.search(pattern, cleaned):
                entities["subject"] = SUBJECT_ALIASES[alias]
                if "lab" in alias:
                    entities["is_lab"] = True
                break

    if "lab" in cleaned or "practical" in cleaned:
        entities["is_lab"] = True

    # 3. Room extraction
    room_match = re.search(r"\b(e\s*[-]?\s*311|e\s*[-]?\s*208)\b", cleaned)
    if room_match:
        rm = room_match.group(0).upper().replace(" ", "")
        if "311" in rm:
            entities["room"] = "E-311"
        elif "208" in rm:
            entities["room"] = "E-208"

    # 4. Semester extraction
    if "odd" in cleaned:
        entities["semester"] = "Odd Semester"
    elif "even" in cleaned:
        entities["semester"] = "Even Semester"
    elif "semester 3" in cleaned or "semester iii" in cleaned or "sem 3" in cleaned:
        entities["semester"] = "Semester III"

    # 5. Month extraction
    for m_name in MONTH_MAP.keys():
        if re.search(r"\b" + re.escape(m_name) + r"\b", cleaned):
            entities["month"] = m_name.capitalize()
            break

    # 6. Specific Date extraction (e.g. 22 December, December 22, 15 June, Christmas)
    date_patterns = [
        r"\b(\d{1,2})(?:st|nd|rd|th)?\s+(january|february|march|april|may|june|july|august|september|october|november|december)\b",
        r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+(\d{1,2})(?:st|nd|rd|th)?\b"
    ]
    for dp in date_patterns:
        dm = re.search(dp, cleaned)
        if dm:
            g1, g2 = dm.groups()
            if g1.isdigit():
                day_num = int(g1)
                m_str = g2.capitalize()
            else:
                day_num = int(g2)
                m_str = g1.capitalize()
            entities["date"] = f"{day_num} {m_str}"
            entities["month"] = m_str
            break

    if "christmas" in cleaned:
        entities["date"] = "25 December"
        entities["month"] = "December"

    # 7. Time & Time of day extraction
    time_match = re.search(r"\b(\d{1,2}(?::\d{2})?)\s*(am|pm)\b", cleaned)
    if time_match:
        entities["time"] = time_match.group(0).upper()
    elif re.search(r"\b11\s*am\b", cleaned):
        entities["time"] = "11:00 AM"
    elif re.search(r"\b10\s*am\b", cleaned):
        entities["time"] = "10:00 AM"
    elif re.search(r"\b12(?::15)?\s*pm\b", cleaned):
        entities["time"] = "12:15 PM"
    elif re.search(r"\b2\s*pm\b", cleaned):
        entities["time"] = "2:00 PM"
    elif re.search(r"\b3\s*pm\b", cleaned):
        entities["time"] = "3:00 PM"

    if "afternoon" in cleaned or "post lunch" in cleaned:
        entities["time_of_day"] = "afternoon"
    elif "morning" in cleaned or "forenoon" in cleaned:
        entities["time_of_day"] = "morning"

    # 8. CA Test extraction
    if re.search(r"\b(ii\s*ca|2nd\s*ca|second\s*ca|ca\s*2)\b", cleaned):
        entities["ca_test"] = "II CA"
    elif re.search(r"\b(i\s*ca|1st\s*ca|first\s*ca|ca\s*1)\b", cleaned):
        entities["ca_test"] = "I CA"
    elif "ca test" in cleaned or "ca tests" in cleaned or "continuous assessment" in cleaned:
        entities["ca_test"] = "CA Tests"

    # 9. Faculty extraction
    if "thara" in cleaned:
        entities["faculty"] = "Dr. L. Thara"
    elif "mohanapriya" in cleaned:
        entities["faculty"] = "Dr. M. Mohanapriya"
    elif "r.k" in cleaned or "rk" in cleaned:
        entities["faculty"] = "Dr. R.K"

    return entities


def detect_intent(text: str, entities: Dict[str, Any]) -> str:
    """Classifies user input into structured semantic intents."""
    cleaned = clean_text(text)

    # 1. Greetings & General Help
    if re.search(r"\b(hi|hello|hey|good morning|good afternoon|help|who are you|what can you do|about)\b", cleaned) and len(cleaned.split()) <= 4:
        return "general_help"

    # 2. Break / Lunch query
    if any(k in cleaned for k in ["lunch break", "lunch time", "lunch period", "what is my lunch", "when is lunch"]):
        return "break_query"
    if any(k in cleaned for k in ["break time", "interval", "what is the break", "recess", "break duration"]):
        return "break_query"

    # Library query
    if "library" in cleaned:
        return "library_query"

    # 3. Next class / upcoming
    if any(k in cleaned for k in ["next class", "next lecture", "what class do i have next", "upcoming class"]):
        return "next_class"

    # 4. Today / Tomorrow schedule
    if any(k in cleaned for k in ["today's schedule", "today timetable", "schedule today", "today's timetable", "classes today", "do i have today"]):
        return "today_schedule"
    if "today" in cleaned and ("schedule" in cleaned or "timetable" in cleaned or "class" in cleaned):
        return "today_schedule"
    if "tomorrow" in cleaned:
        return "tomorrow_schedule"

    # 5. Room query
    if any(k in cleaned for k in ["where is", "which room", "what room is", "room number", "room for", "where does", "location of"]):
        return "room_query"
    if "room" in cleaned and entities.get("subject"):
        return "room_query"

    # 6. Faculty query
    if any(k in cleaned for k in ["who handles", "who teaches", "faculty for", "professor", "handled by", "staff"]):
        return "faculty_query"

    # 7. Lab query (overview of labs)
    if "which subjects have labs" in cleaned or "what labs" in cleaned or "list of labs" in cleaned:
        return "lab_query"

    # 8. Examination fee deadline
    if any(k in cleaned for k in ["fee payment", "examination fee", "exam fee", "fee deadline", "without fine", "with fine"]):
        return "fee_deadline_query"

    # 9. CA Tests query
    if entities.get("ca_test") or "ca test" in cleaned or "ca tests" in cleaned or "cia test" in cleaned:
        return "ca_test_query"

    # 10. Semester dates
    if any(k in cleaned for k in ["semester start", "commence", "classes commence", "commencement of classes", "start of semester", "when does the semester start", "when does the odd semester start", "when does the even semester start"]):
        return "semester_start"
    if any(k in cleaned for k in ["last working day", "semester end", "end of semester", "last day of odd", "last day of even"]):
        return "semester_end"

    # 11. Comprehensive Exam query
    if any(k in cleaned for k in ["comprehensive examination", "comprehensive exam", "final exam", "semester examination", "semester exam", "exam start", "exams commence"]):
        return "exam_query"

    # 12. Holidays
    if any(k in cleaned for k in ["holiday", "holidays", "leave", "vacation"]):
        return "holiday_query"

    # 13. Working days total
    if any(k in cleaned for k in ["working days", "total working days", "number of working days"]):
        return "working_days_query"

    # 14. Which days have a subject (e.g. "Which days have AI?", "Which days have ML?")
    if any(k in cleaned for k in ["which days have", "what days have", "which days do i have", "days with"]):
        return "subject_days_query"

    # 15. Time schedule query (e.g. "What is my class at 11 AM?", "Class at 2 PM")
    if entities.get("time") and not entities.get("subject"):
        return "time_schedule"

    # 16. Subject schedule (e.g. "When is AI on Day III?", "Where/When is ML?", "AI class on Day 3")
    if entities.get("subject"):
        return "subject_schedule"

    # 17. Day schedule (e.g. "What do I have on Day I?", "Show my Day III schedule", "Day 3 afternoon")
    if entities.get("day_order"):
        return "day_schedule"

    # 18. Calendar event query (e.g. "What is the academic event on 22 December?", "events in august")
    if entities.get("date") or (entities.get("month") and not entities.get("subject")):
        return "event_query"
    if any(k in cleaned for k in ["academic calendar", "calendar event", "event on"]):
        return "calendar_query"

    # 19. General Timetable query
    if any(k in cleaned for k in ["timetable", "schedule", "routine", "periods"]):
        return "timetable_query"

    # Default fallback
    return "unknown_query"
