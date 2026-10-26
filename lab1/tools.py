
"""
LAB 1: AGENT VS CHATBOT
Course Management System - Tools

This module provides reusable tools for course management.

Current storage: In-memory demonstration data.
Future upgrade: SQLite database in Lab 2.
"""


# ==================================================
# 1. SAMPLE COURSE DATA
# ==================================================

COURSES = [
    {
        "id": 1,
        "name": "Database Management Systems",
        "semester": 7,
        "department": "Computer Science",
        "description": "SQL, relational databases, and database design."
    },
    {
        "id": 2,
        "name": "Artificial Intelligence",
        "semester": 7,
        "department": "Computer Science",
        "description": "Search, reasoning, intelligent agents, and AI."
    },
    {
        "id": 3,
        "name": "Computer Networks",
        "semester": 6,
        "department": "Computer Science",
        "description": "Networking protocols and communication systems."
    },
    {
        "id": 4,
        "name": "Machine Learning",
        "semester": 7,
        "department": "Computer Science",
        "description": "Supervised learning and unsupervised learning."
    },
    {
        "id": 5,
        "name": "Cloud Computing",
        "semester": 6,
        "department": "Computer Science",
        "description": "Cloud infrastructure and deployment."
    },
    {
        "id": 6,
        "name": "Deep Learning",
        "semester": 7,
        "department": "Computer Science",
        "description": "Neural networks and deep learning architectures."
    },
    {
        "id": 7,
        "name": "Computer Vision",
        "semester": 7,
        "department": "Computer Science",
        "description": "Image processing and object detection."
    },
    {
        "id": 8,
        "name": "Operating Systems",
        "semester": 5,
        "department": "Computer Science",
        "description": "Processes and memory management."
    }
]


# ==================================================
# 2. COUNT COURSES
# ==================================================

def count_courses():
    """Return the total number of courses."""
    return len(COURSES)


# ==================================================
# 3. LIST COURSES
# ==================================================

def list_courses():
    """Return all registered courses."""
    return [course.copy() for course in COURSES]


# ==================================================
# 4. SEARCH COURSES
# ==================================================

def find_course(course_name):
    """Search courses using a full or partial name."""

    query = course_name.strip().casefold()

    if not query:
        return []

    return [
        course.copy()
        for course in COURSES
        if query in course["name"].casefold()
    ]


# ==================================================
# 5. GET COURSE DETAILS BY ID
# ==================================================

def get_course_details(course_id):
    """Retrieve course information using its ID."""

    if not isinstance(course_id, int) or isinstance(course_id, bool):
        raise ValueError("Course ID must be an integer.")

    for course in COURSES:
        if course["id"] == course_id:
            return course.copy()

    return None


# ==================================================
# 6. FILTER COURSES BY SEMESTER
# ==================================================

def list_courses_by_semester(semester):
    """Return courses belonging to a specified semester."""

    if not isinstance(semester, int) or isinstance(semester, bool):
        raise ValueError("Semester must be an integer.")

    if not 1 <= semester <= 12:
        raise ValueError("Semester must be between 1 and 12.")

    return [
        course.copy()
        for course in COURSES
        if course["semester"] == semester
    ]


# ==================================================
# 7. COURSE SUMMARY
# ==================================================

def get_course_summary():
    """Generate a summary of registered courses."""

    semester_counts = {}
    department_counts = {}

    for course in COURSES:
        semester = course["semester"]
        department = course["department"]

        semester_counts[semester] = (
            semester_counts.get(semester, 0) + 1
        )

        department_counts[department] = (
            department_counts.get(department, 0) + 1
        )

    return {
        "total_courses": len(COURSES),
        "semesters": semester_counts,
        "departments": sorted(department_counts.keys()),
        "department_counts": department_counts
    }


# ==================================================
# 8. TEST TOOLS INDEPENDENTLY
# ==================================================

if __name__ == "__main__":

    print("=== COURSE MANAGEMENT TOOLS ===")

    print("\nTotal courses:", count_courses())

    print("\nAll courses:")

    for course in list_courses():
        print(
            f"{course['id']}. {course['name']} "
            f"(Semester {course['semester']})"
        )

    print("\nSearching for Artificial Intelligence:")

    print(find_course("Artificial Intelligence"))

    print("\nDetails of course ID 2:")

    print(get_course_details(2))

    print("\nCourses in semester 7:")

    print(list_courses_by_semester(7))

    print("\nCourse summary:")

    print(get_course_summary())

