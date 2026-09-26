from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    class_type = Column(String(50), nullable=False)  # Theory, Practical/Lab, Major Elective
    faculty = Column(String(200), nullable=True)

    # Relationships
    timetable_entries = relationship("Timetable", back_populates="subject_rel")


class Timetable(Base):
    __tablename__ = "timetable"

    id = Column(Integer, primary_key=True, index=True)
    day_order = Column(String(20), index=True, nullable=False)  # Day I, Day II, etc.
    start_time = Column(String(20), nullable=False)  # "10:00 AM"
    end_time = Column(String(20), nullable=False)    # "11:00 AM"
    subject = Column(String(100), nullable=False)    # "AI", "ML Lab", "Break"
    room = Column(String(50), nullable=True)         # "E-311", "E-208"
    faculty = Column(String(200), nullable=True)     # "Dr. L. Thara & Dr. R.K"
    class_type = Column(String(50), nullable=False)  # "Theory", "Lab", "Break", "Lunch"
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)

    # Relationships
    subject_rel = relationship("Subject", back_populates="timetable_entries")


class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(20), index=True, nullable=False)  # "YYYY-MM-DD" e.g. "2026-06-15"
    day = Column(String(20), nullable=False)               # "Monday"
    event = Column(String(250), nullable=False)            # "Commencement of Classes"
    category = Column(String(100), index=True, nullable=False)  # "Semester Date", "Holiday", "CA Test", "Examination", "Fee Payment", "Academic Event"
    semester = Column(String(50), index=True, nullable=True)    # "Odd Semester", "Even Semester", "Both"
    is_holiday = Column(Boolean, default=False, nullable=False)
    description = Column(Text, nullable=True)
