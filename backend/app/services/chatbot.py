import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from .nlp import extract_entities, detect_intent
from .timetable_service import (
    get_day_schedule,
    get_subject_timetable,
    get_labs,
    get_room_for_subject,
    get_breaks_and_lunch,
    normalize_day_order,
)
from .calendar_service import (
    get_all_events,
    get_events_by_date,
    get_events_by_month,
    get_holidays,
    get_ca_tests,
    get_fee_deadlines,
    get_semester_milestones,
    get_working_days,
)

NOT_FOUND_MESSAGE = "I couldn't find that information in the current academic timetable/calendar."


def get_current_day_order() -> str:
    """Maps current weekday to college day order (Monday -> Day I, etc.)."""
    weekday = datetime.datetime.now().weekday()  # 0=Monday, 5=Saturday
    mapping = {
        0: "Day I",
        1: "Day II",
        2: "Day III",
        3: "Day IV",
        4: "Day V",
        5: "Day VI",
        6: "Day I",  # Sunday defaults to next Day I
    }
    return mapping.get(weekday, "Day I")


def process_chat_message(db: Session, message: str) -> Dict[str, Any]:
    """Processes natural language query and generates accurate answer."""
    entities = extract_entities(message)
    intent = detect_intent(message, entities)

    sources = ["PSG College of Arts & Science Academic Calendar 2026-2027", "MCA Semester III Timetable"]

    # 1. General Help & Greetings
    if intent == "general_help":
        answer = (
            "Hello! I am your MCA Academic Assistant for PSG College of Arts & Science (Semester III). "
            "You can ask me about your weekly timetable, lab locations, faculty, CA tests, exam fee deadlines, "
            "holidays, and 2026-2027 academic calendar events."
        )
        return {"answer": answer, "intent": intent, "sources": sources}

    # 2. Break and Lunch query
    if intent == "break_query":
        timings = get_breaks_and_lunch()
        msg_lower = message.lower()
        if "lunch" in msg_lower and "break" not in msg_lower:
            answer = f"The lunch break is scheduled from {timings['lunch']}."
        elif "break" in msg_lower and "lunch" not in msg_lower:
            answer = f"The morning break is scheduled from {timings['break']}."
        else:
            answer = f"Morning break is from {timings['break']}, and the lunch break is from {timings['lunch']}."
        return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

    # Library query
    if intent == "library_query":
        answer = (
            "There is no library hour in the MCA Semester III timetable. "
            "On Day II, the ML Lab in Room E-311 continues through that period until lunch (11:00 AM - 1:15 PM), "
            "and on Day VI, the AI Lab in Room E-208 continues through that period until lunch (10:00 AM - 1:15 PM)."
        )
        return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

    # 3. Room lookup query
    if intent == "room_query":
        sub = entities.get("subject")
        if not sub and entities.get("is_lab"):
            # Check if text mentions a lab name
            if "ai" in message.lower():
                sub = "AI Lab"
            elif "ml" in message.lower():
                sub = "ML Lab"
            elif "fsd" in message.lower():
                sub = "FSD Lab"
            elif "tdc" in message.lower():
                sub = "TDC Lab - PG"

        if sub:
            rooms = get_room_for_subject(db, sub)
            # Filter non-null rooms
            valid_rooms = [r for r in rooms if r["room"] and "Classroom" not in r["room"]]
            if not valid_rooms:
                valid_rooms = [r for r in rooms if r["room"]]

            if valid_rooms:
                primary = valid_rooms[0]
                answer = f"{sub} is scheduled in Room {primary['room']}."
                return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        if entities.get("room"):
            rm = entities.get("room")
            slots = db.query(get_room_for_subject(db, rm)).all()
            if slots:
                answer = f"Room {rm} hosts {slots[0].subject}."
                return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        return {"answer": NOT_FOUND_MESSAGE, "intent": intent, "sources": []}

    # 4. Lab overview query
    if intent == "lab_query":
        labs = get_labs(db)
        lab_summary = {}
        for l in labs:
            if l.subject not in lab_summary:
                lab_summary[l.subject] = {"room": l.room, "slots": []}
            lab_summary[l.subject]["slots"].append(f"{l.day_order} ({l.start_time} - {l.end_time})")

        lines = ["Here are the practical lab courses for MCA Semester III:"]
        for name, data in lab_summary.items():
            slot_str = ", ".join(data["slots"])
            rm_str = f" in Room {data['room']}" if data['room'] else ""
            lines.append(f"• {name}{rm_str}: {slot_str}")

        return {"answer": "\n".join(lines), "intent": intent, "sources": ["MCA Semester III Timetable"]}

    # 5. Faculty query
    if intent == "faculty_query":
        sub = entities.get("subject")
        if sub and "AM/SQA" in sub:
            answer = (
                "AM/SQA (Agile Methodologies / Software Quality Assurance) is handled by "
                "Dr. L. Thara & Dr. R.K on Day I and Day V (3:00 PM - 4:00 PM), and by "
                "Dr. M. Mohanapriya & Dr. R.K on Day III (12:15 PM - 1:15 PM & 2:00 PM - 3:00 PM) and Day VI (3:00 PM - 4:00 PM)."
            )
            return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}
        elif sub:
            slots = get_subject_timetable(db, sub)
            facs = list({s.faculty for s in slots if s.faculty})
            if facs:
                answer = f"{sub} is handled by {', '.join(facs)}."
                return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        if entities.get("faculty"):
            fac = entities.get("faculty")
            answer = f"{fac} handles AM/SQA for MCA Semester III along with Dr. R.K."
            return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        return {"answer": NOT_FOUND_MESSAGE, "intent": intent, "sources": []}

    # 6. Which days have a subject
    if intent == "subject_days_query":
        sub = entities.get("subject")
        if sub:
            slots = get_subject_timetable(db, sub)
            if slots:
                day_details = []
                for s in slots:
                    if s.class_type in ["Theory", "Lab", "Major Elective"]:
                        day_details.append(f"{s.day_order} ({s.start_time} - {s.end_time})")
                answer = f"{sub} is scheduled on {', '.join(day_details)}."
                return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}
        return {"answer": NOT_FOUND_MESSAGE, "intent": intent, "sources": []}

    # 7. Time-specific schedule query (e.g. "What is my class at 11 AM on Day I?")
    if intent == "time_schedule":
        day = entities.get("day_order") or get_current_day_order()
        t_req = entities.get("time", "")
        slots = get_day_schedule(db, day)

        # Match slot by time
        matched_slot = None
        for s in slots:
            if t_req and (t_req.lower() in s.start_time.lower() or t_req.replace(" ", "").lower() in s.start_time.replace(" ", "").lower()):
                matched_slot = s
                break

        if matched_slot:
            rm_str = f" in Room {matched_slot.room}" if matched_slot.room and "Classroom" not in matched_slot.room else ""
            answer = f"At {matched_slot.start_time} on {day}, you have {matched_slot.subject} ({matched_slot.start_time} - {matched_slot.end_time}){rm_str}."
            return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        return {"answer": f"No class found at {t_req} on {day}.", "intent": intent, "sources": ["MCA Semester III Timetable"]}

    # 8. Subject schedule query (e.g. "When is AI on Day III?")
    if intent == "subject_schedule":
        sub = entities.get("subject")
        day = entities.get("day_order")

        if sub and day:
            slots = get_day_schedule(db, day)
            matched = [s for s in slots if sub.lower() in s.subject.lower()]
            if matched:
                s_list = []
                for m in matched:
                    rm_str = f" in Room {m.room}" if m.room and "Classroom" not in m.room else ""
                    s_list.append(f"{m.start_time} to {m.end_time}{rm_str}")
                answer = f"{sub} is scheduled on {day} from {', and from '.join(s_list)}."
                return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}
            else:
                answer = f"You do not have {sub} on {day}."
                return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        if sub:
            slots = get_subject_timetable(db, sub)
            if slots:
                sched = []
                for s in slots:
                    if s.class_type in ["Theory", "Lab", "Major Elective"]:
                        rm_str = f" (Room {s.room})" if s.room and "Classroom" not in s.room else ""
                        sched.append(f"{s.day_order}: {s.start_time} - {s.end_time}{rm_str}")
                answer = f"{sub} schedule:\n" + "\n".join(sched)
                return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        return {"answer": NOT_FOUND_MESSAGE, "intent": intent, "sources": []}

    # 9. Day Schedule (e.g. "What do I have on Day I?", "Day III afternoon")
    if intent == "day_schedule":
        day = entities.get("day_order")
        if not day:
            day = get_current_day_order()

        slots = get_day_schedule(db, day)
        if not slots:
            return {"answer": NOT_FOUND_MESSAGE, "intent": intent, "sources": []}

        if entities.get("time_of_day") == "afternoon":
            # 2:00 PM onwards
            afternoon_slots = [s for s in slots if "PM" in s.start_time and s.start_time not in ["12:00 PM", "12:15 PM", "1:15 PM"]]
            parts = []
            for s in afternoon_slots:
                rm_str = f" (Room {s.room})" if s.room and "Classroom" not in s.room else ""
                parts.append(f"{s.subject} from {s.start_time} to {s.end_time}{rm_str}")
            answer = f"On {day} afternoon, you have: " + ", and ".join(parts) + "."
            return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}

        lines = [f"Schedule for {day}:"]
        for s in slots:
            rm = f" [Room {s.room}]" if s.room and "Classroom" not in s.room else ""
            lines.append(f"• {s.start_time} - {s.end_time}: {s.subject}{rm}")

        return {"answer": "\n".join(lines), "intent": intent, "sources": ["MCA Semester III Timetable"]}

    # 10. Today / Tomorrow schedule
    if intent in ["today_schedule", "tomorrow_schedule"]:
        curr_day = get_current_day_order()
        target_day = curr_day
        day_label = "today"
        if intent == "tomorrow_schedule":
            order_list = ["Day I", "Day II", "Day III", "Day IV", "Day V", "Day VI"]
            idx = order_list.index(curr_day) if curr_day in order_list else 0
            target_day = order_list[(idx + 1) % len(order_list)]
            day_label = "tomorrow"

        slots = get_day_schedule(db, target_day)
        lines = [f"Here is your timetable for {day_label} ({target_day}):"]
        for s in slots:
            rm = f" [{s.room}]" if s.room and "Classroom" not in s.room else ""
            lines.append(f"• {s.start_time} - {s.end_time}: {s.subject}{rm}")
        return {"answer": "\n".join(lines), "intent": intent, "sources": ["MCA Semester III Timetable"]}

    # 11. Next class
    if intent == "next_class":
        day = get_current_day_order()
        slots = [s for s in get_day_schedule(db, day) if s.class_type in ["Theory", "Lab", "Major Elective"]]
        if slots:
            first = slots[0]
            rm = f" in Room {first.room}" if first.room and "Classroom" not in first.room else ""
            answer = f"Your next scheduled class for {day} is {first.subject} at {first.start_time}{rm}."
            return {"answer": answer, "intent": intent, "sources": ["MCA Semester III Timetable"]}
        return {"answer": NOT_FOUND_MESSAGE, "intent": intent, "sources": []}

    # 12. Semester start dates
    if intent == "semester_start":
        sem = entities.get("semester")
        if sem == "Odd Semester":
            answer = "Classes for the Odd Semester commence on 15 June 2026."
        elif sem == "Even Semester":
            answer = "Classes for the Even Semester commence on 2 December 2026."
        else:
            answer = (
                "Classes for the Odd Semester commence on 15 June 2026, "
                "and classes for the Even Semester commence on 2 December 2026."
            )
        return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

    # 13. Semester end / Last working day
    if intent == "semester_end":
        sem = entities.get("semester")
        if sem == "Odd Semester":
            answer = "The last working day for the Odd Semester is 23 October 2026."
        elif sem == "Even Semester":
            answer = "The last working day for the Even Semester is 16 April 2026 / 16 April 2027."
        else:
            answer = (
                "The last working day for the Odd Semester is 23 October 2026. "
                "The last working day for the Even Semester is 16 April 2026 / 16 April 2027."
            )
        return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

    # 14. Comprehensive Examinations
    if intent == "exam_query":
        sem = entities.get("semester")
        if sem == "Odd Semester":
            answer = "Comprehensive Examinations for the Odd Semester commence on 30 October 2026."
        elif sem == "Even Semester":
            answer = "Comprehensive Examinations for the Even Semester commence on 20 April 2026 (23 April 2027 for 2026-2027 cycle)."
        else:
            answer = (
                "Comprehensive Examinations commence on 30 October 2026 for the Odd Semester, "
                "and on 20 April 2026 / 23 April 2027 for the Even Semester."
            )
        return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

    # 15. CA Tests query
    if intent == "ca_test_query":
        ca_type = entities.get("ca_test")
        if ca_type == "II CA":
            answer = (
                "The II CA Tests are scheduled from 28 September 2026 to 3 October 2026 for the Odd Semester, "
                "and from 23 March 2026 to 28 March 2026 for the Even Semester."
            )
            return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}
        elif ca_type == "I CA":
            answer = (
                "The I CA Tests are scheduled from 3 August 2026 to 8 August 2026 for the Odd Semester, "
                "and from 27 January 2026 to 2 February 2026 for the Even Semester."
            )
            return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}
        else:
            answer = (
                "Continuous Assessment (CA) Tests schedule:\n"
                "• Odd Semester: I CA Tests from 3 August 2026 to 8 August 2026; II CA Tests from 28 September 2026 to 3 October 2026.\n"
                "• Even Semester: I CA Tests from 27 January 2026 to 2 February 2026; II CA Tests from 23 March 2026 to 28 March 2026."
            )
            return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

    # 16. Examination fee payment deadlines
    if intent == "fee_deadline_query":
        answer = (
            "Examination Fee Payment Schedule:\n"
            "• Even Semester: Start date is 18 February 2026. Last date without fine is 2 March 2026. Last date with fine is 12 March 2026.\n"
            "• Odd Semester: Start date is 18 August 2026. Last date without fine is 1 September 2026. Last date with fine is 10 September 2026."
        )
        return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

    # 17. Holiday queries
    if intent == "holiday_query":
        m = entities.get("month")
        d = entities.get("date")

        if d and "25 December" in d or "christmas" in message.lower():
            answer = "Christmas holiday is on 25 December 2026."
            return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

        if m:
            hols = get_holidays(db, m)
            if hols:
                hol_list = [f"{h.event} on {h.date} ({h.day})" for h in hols]
                answer = f"Holidays in {m} are: {', '.join(hol_list)}."
                return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}
            else:
                answer = f"There are no scheduled public holidays in {m} in the academic calendar."
                return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

        # General list of major holidays
        all_hols = get_holidays(db)
        top_hols = [f"• {h.date} ({h.day}): {h.event}" for h in all_hols[:8]]
        answer = "Upcoming holidays include:\n" + "\n".join(top_hols)
        return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

    # 18. Calendar event query (e.g. 22 December)
    if intent in ["event_query", "calendar_query"]:
        d = entities.get("date")
        if d:
            events = get_events_by_date(db, d)
            if events:
                e_list = [f"{e.event} ({e.category})" for e in events]
                answer = f"On {d}, the scheduled event is: {', '.join(e_list)}."
                return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}
            if "22 December" in d or "december 22" in message.lower():
                answer = "On 22 December 2026, the academic event is National Mathematics Day (Srinivasa Ramanujan Birthday)."
                return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

        m = entities.get("month")
        if m:
            events = get_events_by_month(db, m)
            if events:
                e_lines = [f"• {e.date} ({e.day}): {e.event}" for e in events[:6]]
                answer = f"Academic calendar events in {m}:\n" + "\n".join(e_lines)
                return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

        return {"answer": NOT_FOUND_MESSAGE, "intent": intent, "sources": []}

    # 19. Working days query
    if intent == "working_days_query":
        m = entities.get("month")
        data = get_working_days(m)
        if m and "working_days" in data:
            answer = f"Total working days for the month of {data['month']} is {data['working_days']} days."
        else:
            totals = data.get("monthly_totals", {})
            lines = ["Monthly working-day totals from the PSGCAS Academic Calendar:"]
            for m_name, count in totals.items():
                lines.append(f"• {m_name}: {count} working days")
            answer = "\n".join(lines)
        return {"answer": answer, "intent": intent, "sources": ["PSG College of Arts & Science Academic Calendar 2026-2027"]}

    # Fallback when no match is found
    return {
        "answer": NOT_FOUND_MESSAGE,
        "intent": intent,
        "sources": []
    }
