from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Subject
from ..schemas import SubjectDetailResponse, SubjectScheduleSlot

router = APIRouter(prefix="/api/subjects", tags=["Subjects"])


@router.get("", response_model=List[SubjectDetailResponse])
def get_all_subjects(db: Session = Depends(get_db)):
    """Retrieves all MCA Semester III subjects with their scheduled days and times."""
    subjects = db.query(Subject).all()
    results = []
    for s in subjects:
        slots = []
        for t in s.timetable_entries:
            slots.append(
                SubjectScheduleSlot(
                    day_order=t.day_order,
                    start_time=t.start_time,
                    end_time=t.end_time,
                    room=t.room,
                    faculty=t.faculty,
                    class_type=t.class_type,
                )
            )
        results.append(
            SubjectDetailResponse(
                id=s.id,
                code=s.code,
                name=s.name,
                description=s.description,
                class_type=s.class_type,
                faculty=s.faculty,
                schedules=slots,
            )
        )
    return results


@router.get("/{code_or_name}", response_model=SubjectDetailResponse)
def get_subject_detail(code_or_name: str, db: Session = Depends(get_db)):
    """Retrieves specific subject by code or name."""
    clean = code_or_name.strip().lower()
    subject = db.query(Subject).filter(
        (Subject.code.ilike(f"%{clean}%")) | (Subject.name.ilike(f"%{clean}%"))
    ).first()
    if not subject:
        raise HTTPException(status_code=404, detail=f"Subject '{code_or_name}' not found.")

    slots = [
        SubjectScheduleSlot(
            day_order=t.day_order,
            start_time=t.start_time,
            end_time=t.end_time,
            room=t.room,
            faculty=t.faculty,
            class_type=t.class_type,
        )
        for t in subject.timetable_entries
    ]
    return SubjectDetailResponse(
        id=subject.id,
        code=subject.code,
        name=subject.name,
        description=subject.description,
        class_type=subject.class_type,
        faculty=subject.faculty,
        schedules=slots,
    )
