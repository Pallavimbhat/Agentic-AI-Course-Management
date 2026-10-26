"""
LAB 3: COURSE MANAGEMENT SKILL

A reusable skill for retrieving, searching, and summarizing courses.
"""

from lab2.tools import (
    count_courses,
    list_courses,
    find_course,
    get_course_summary,
)


class CourseManagementSkill:
    """Reusable skill for course-related operations."""

    name = "course_management"

    description = (
        "Lists courses, counts courses, searches for courses, "
        "and generates course summaries."
    )

    instructions = [
        "Use list_courses to retrieve all courses.",
        "Use count_courses to count stored courses.",
        "Use find_course to search by course name.",
        "Use get_course_summary to summarize courses by semester.",
    ]

    def execute(self, action, query=None):
        """Execute a course-management operation."""

        if action == "list":
            return list_courses()

        if action == "count":
            return {
                "total_courses": count_courses()
            }

        if action == "search":
            if not query or not query.strip():
                return {
                    "error": "Provide a course name to search."
                }

            return find_course(query)

        if action == "summary":
            return get_course_summary()

        return {
            "error": f"Unsupported course action: {action}"
        }