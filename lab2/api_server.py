
"""
LAB 2: Local Course Management API

Run with:
python -m uvicorn lab2.api_server:app --reload --port 8000

The API exposes read-only course operations.
"""

from fastapi import FastAPI, HTTPException

from lab2.tools import (
    count_courses,
    list_courses,
    find_course,
    get_course_summary,
)

app = FastAPI(
    title="Course Management API",
    description="API for the Agentic AI Course Management System",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Course Management API is running",
        "endpoints": [
            "/health",
            "/courses",
            "/courses/count",
            "/courses/search?q=Artificial",
            "/courses/summary",
        ],
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/courses")
def courses():
    return {"courses": list_courses()}


@app.get("/courses/count")
def courses_count():
    return {"count": count_courses()}


@app.get("/courses/search")
def search_courses(q: str):
    results = find_course(q)

    return {
        "query": q,
        "matches": results,
    }


@app.get("/courses/summary")
def courses_summary():
    return get_course_summary()
