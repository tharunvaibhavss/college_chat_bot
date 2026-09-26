import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.seed.seed_database import seed_data

client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Ensure database has seed data before running tests."""
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


def test_health_check():
    """Verify health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "version" in data


def test_timetable_retrieval():
    """1. Test full timetable retrieval."""
    response = client.get("/api/timetable")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    subjects = [item["subject"] for item in data]
    assert "AI" in subjects
    assert "ML" in subjects


def test_day_schedule():
    """3. Test day schedule retrieval."""
    response = client.get("/api/timetable/day/Day%20I")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    first_slot = data[0]
    assert first_slot["start_time"] == "10:00 AM"


def test_subject_retrieval():
    """2. Test subjects retrieval."""
    response = client.get("/api/subjects")
    assert response.status_code == 200
    data = response.json()
    codes = [s["code"] for s in data]
    assert "25CAP314" in codes  # AI
    assert "25CAP315" in codes  # ML


def test_calendar_retrieval():
    """5. Test calendar retrieval."""
    response = client.get("/api/calendar")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 10


def test_holiday_lookup():
    """6. Test holiday lookup."""
    response = client.get("/api/calendar/holidays")
    assert response.status_code == 200
    data = response.json()
    events = [h["event"] for h in data]
    assert any("Independence Day" in e for e in events)
    assert any("Pongal" in e for e in events)


def test_chat_room_lookup():
    """4. Room lookup through chatbot: 'Where is ML Lab?' and 'What room is FSD Lab?'"""
    res1 = client.post("/api/chat", json={"message": "Where is ML Lab?"})
    assert res1.status_code == 200
    assert "E-311" in res1.json()["answer"]
    assert res1.json()["intent"] == "room_query"

    res2 = client.post("/api/chat", json={"message": "What room is FSD Lab?"})
    assert res2.status_code == 200
    assert "E-208" in res2.json()["answer"]


def test_chat_day_schedule():
    """Chatbot query: 'What do I have on Day I?'"""
    res = client.post("/api/chat", json={"message": "What do I have on Day I?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "TDC (PG)" in ans
    assert "AI" in ans
    assert "ML" in ans


def test_chat_subject_schedule():
    """Chatbot query: 'When is AI on Day III?'"""
    res = client.post("/api/chat", json={"message": "When is AI on Day III?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "3:00 PM" in ans
    assert "5:00 PM" in ans


def test_chat_semester_dates():
    """7. Semester dates: 'When does the odd semester start?' and 'When does the even semester start?'"""
    res_odd = client.post("/api/chat", json={"message": "When does the odd semester start?"})
    assert res_odd.status_code == 200
    assert "15 June 2026" in res_odd.json()["answer"]

    res_even = client.post("/api/chat", json={"message": "When does the even semester start?"})
    assert res_even.status_code == 200
    assert "2 December 2026" in res_even.json()["answer"]

    res_end = client.post("/api/chat", json={"message": "When is the last working day of the even semester?"})
    assert res_end.status_code == 200
    assert "16 April" in res_end.json()["answer"]


def test_chat_ca_tests():
    """8. CA test query: 'When are the II CA Tests?'"""
    res = client.post("/api/chat", json={"message": "When are the II CA Tests?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "28 September" in ans or "23 March" in ans


def test_chat_christmas_holiday():
    """Chatbot query: 'When is Christmas holiday?'"""
    res = client.post("/api/chat", json={"message": "When is Christmas holiday?"})
    assert res.status_code == 200
    assert "25 December 2026" in res.json()["answer"]


def test_chat_lunch_time():
    """Chatbot query: 'What is my lunch time?'"""
    res = client.post("/api/chat", json={"message": "What is my lunch time?"})
    assert res.status_code == 200
    assert "1:15 PM" in res.json()["answer"]
    assert "2:00 PM" in res.json()["answer"]


def test_chat_faculty():
    """Chatbot query: 'Who handles AM/SQA?'"""
    res = client.post("/api/chat", json={"message": "Who handles AM/SQA?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "Dr. L. Thara" in ans
    assert "Dr. R.K" in ans
    assert "Dr. M. Mohanapriya" in ans


def test_chat_august_holidays():
    """Chatbot query: 'What are the holidays in August?'"""
    res = client.post("/api/chat", json={"message": "What are the holidays in August?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "Independence Day" in ans


def test_chat_december_22_event():
    """Chatbot query: 'What is the academic event on 22 December?'"""
    res = client.post("/api/chat", json={"message": "What is the academic event on 22 December?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "National Mathematics Day" in ans


def test_chat_fee_deadline():
    """Chatbot query: 'When is the examination fee payment deadline?'"""
    res = client.post("/api/chat", json={"message": "When is the examination fee payment deadline?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "18 February 2026" in ans or "2 March 2026" in ans


def test_chat_which_days_have_ai():
    """Chatbot query: 'Which days have AI?'"""
    res = client.post("/api/chat", json={"message": "Which days have AI?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "Day I" in ans
    assert "Day III" in ans


def test_chat_which_subjects_have_labs():
    """Chatbot query: 'Which subjects have labs?'"""
    res = client.post("/api/chat", json={"message": "Which subjects have labs?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "AI Lab" in ans
    assert "ML Lab" in ans
    assert "FSD Lab" in ans


def test_chat_unknown_question():
    """10. Test unknown question guardrail."""
    res = client.post("/api/chat", json={"message": "Tell me something that isn't in the database."})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "I couldn't find that information in the current academic timetable/calendar." in ans


def test_chat_no_library_hour():
    """Test that there is no library hour and lab continues."""
    res = client.post("/api/chat", json={"message": "When is library hour?"})
    assert res.status_code == 200
    ans = res.json()["answer"]
    assert "no library hour" in ans.lower()
    assert "ML Lab" in ans
    assert "AI Lab" in ans

