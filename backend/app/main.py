from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .models import Subject
from .seed.seed_database import seed_data
from .routes import chat, timetable, calendar, subjects
from .schemas import HealthResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database schema is created
    Base.metadata.create_all(bind=engine)

    # Check if database needs seeding
    db = SessionLocal()
    try:
        subject_count = db.query(Subject).count()
        if subject_count == 0:
            print("Database empty. Seeding initial academic data...")
            seed_data(db)
            print("Database seeded successfully.")
    finally:
        db.close()

    yield


app = FastAPI(
    title="MCA Academic Assistant API",
    description="Backend API for PSG College of Arts & Science MCA Semester III Timetable & Academic Calendar Chatbot",
    version="1.0.0",
    lifespan=lifespan,
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Next.js development server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(chat.router)
app.include_router(timetable.router)
app.include_router(calendar.router)
app.include_router(subjects.router)


@app.get("/api/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Health check endpoint to verify backend service status."""
    return {
        "status": "online",
        "message": "MCA Academic Assistant API is healthy and operational.",
        "version": "1.0.0",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
