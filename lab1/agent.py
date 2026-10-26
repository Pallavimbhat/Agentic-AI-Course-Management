
"""
LAB 1: AGENT VS CHATBOT
Course Management Agent

This rule-based agent interprets supported requests,
selects registered tools, executes them, and returns results.

It is a tool-using agent prototype, not an LLM-powered agent.
"""

import re

from tools import (
    count_courses,
    list_courses,
    find_course,
    get_course_details,
    list_courses_by_semester,
    get_course_summary,
)


# ==================================================
# 1. TOOL REGISTRY
# ==================================================

TOOLS = {
    "count_courses": {
        "description": "Count all registered courses.",
        "function": count_courses
    },
    "list_courses": {
        "description": "List all registered courses.",
        "function": list_courses
    },
    "find_course": {
        "description": "Search courses by name.",
        "function": find_course
    },
    "get_course_details": {
        "description": "Retrieve course details by ID.",
        "function": get_course_details
    },
    "list_courses_by_semester": {
        "description": "Filter courses by semester.",
        "function": list_courses_by_semester
    },
    "get_course_summary": {
        "description": "Summarize course information.",
        "function": get_course_summary
    }
}


# ==================================================
# 2. SAFE TOOL EXECUTION
# ==================================================

def execute_tool(tool_name, **kwargs):
    """Execute a registered tool and handle errors."""

    tool = TOOLS.get(tool_name)

    if tool is None:
        return {
            "success": False,
            "error": "The requested tool is unavailable."
        }

    try:
        result = tool["function"](**kwargs)

        return {
            "success": True,
            "result": result
        }

    except (TypeError, ValueError):
        return {
            "success": False,
            "error": "Invalid input for this operation."
        }

    except Exception:
        return {
            "success": False,
            "error": "An unexpected error occurred."
        }


# ==================================================
# 3. FORMAT COURSE RESULTS
# ==================================================

def format_courses(courses):

    if not courses:
        return "No matching courses were found."

    output = []

    for course in courses:
        output.append(
            f"- {course['name']} "
            f"(ID: {course['id']}, "
            f"Semester: {course['semester']}, "
            f"Department: {course['department']})"
        )

    return "\n".join(output)


def format_summary(summary):

    output = [
        f"Total courses: {summary['total_courses']}",
        "",
        "Courses by semester:"
    ]

    for semester, count in sorted(summary["semesters"].items()):
        output.append(f"- Semester {semester}: {count}")

    output.append(
        "Departments: " + ", ".join(summary["departments"])
    )

    return "\n".join(output)


# ==================================================
# 4. REQUEST ROUTING
# ==================================================

def run_agent(user_message):
    """Interpret a supported request and execute its tool."""

    message = " ".join(user_message.strip().split())
    text = message.casefold()

    if not text:
        return "Please enter a message."

    # ---------------- HELP ----------------

    if text in {
        "help",
        "commands",
        "what can you do",
        "what can you help me with"
    }:
        return """
COURSE MANAGEMENT AGENT

Examples of supported requests:

1. Count courses
   How many courses are available?

2. List courses
   Show me all courses.

3. Search for a course
   Find Artificial Intelligence.

4. Retrieve course details
   Show course ID 2.

5. Filter by semester
   Which courses are in semester 7?

6. Generate a summary
   Give me a course summary.

7. List available tools
   List tools.

Type 'exit' to quit.
"""

    # ---------------- TOOL DISCOVERY ----------------

    if text in {
        "list tools",
        "show tools",
        "available tools",
        "what tools do you have"
    }:
        output = ["Registered tools:"]

        for name, details in TOOLS.items():
            output.append(
                f"- {name}: {details['description']}"
            )

        return "\n".join(output)

    # ---------------- GREETINGS ----------------

    if text in {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    }:
        return (
            "Hello! I am your Course Management Agent. "
            "Ask me to search, list, count, or analyze courses. "
            "Type 'help' for examples."
        )

    # ---------------- COUNT COURSES ----------------

    count_pattern = (
        r"\b(count|number|total|quantity|how many|how much)\b"
    )

    course_pattern = r"\b(courses?|subjects?)\b"

    asks_count = bool(re.search(count_pattern, text))
    mentions_courses = bool(re.search(course_pattern, text))

    if asks_count and mentions_courses:

        result = execute_tool("count_courses")

        if result["success"]:
            return (
                f"There are {result['result']} "
                "courses registered in the system."
            )

        return result["error"]

    # ---------------- COURSE SUMMARY ----------------

    if (
        any(word in text for word in (
            "summary",
            "overview",
            "breakdown"
        ))
        and mentions_courses
    ):

        result = execute_tool("get_course_summary")

        if result["success"]:
            return format_summary(result["result"])

        return result["error"]

    # ---------------- COURSE ID LOOKUP ----------------

    id_match = re.search(
        r"\b(?:course\s*)?id\s*#?\s*(\d+)\b",
        text
    )

    if id_match:

        course_id = int(id_match.group(1))

        result = execute_tool(
            "get_course_details",
            course_id=course_id
        )

        if not result["success"]:
            return result["error"]

        course = result["result"]

        if course is None:
            return f"No course exists with ID {course_id}."

        return (
            f"Course: {course['name']}\n"
            f"ID: {course['id']}\n"
            f"Semester: {course['semester']}\n"
            f"Department: {course['department']}\n"
            f"Description: {course['description']}"
        )

    # ---------------- SEMESTER FILTER ----------------

    semester_match = re.search(
        r"\bsemester\s*(\d+)\b",
        text
    )

    if semester_match and mentions_courses:

        semester = int(semester_match.group(1))

        if not 1 <= semester <= 12:
            return "Please provide a semester between 1 and 12."

        result = execute_tool(
            "list_courses_by_semester",
            semester=semester
        )

        if not result["success"]:
            return result["error"]

        return (
            f"Courses in semester {semester}:\n"
            + format_courses(result["result"])
        )

    # ---------------- LIST COURSES ----------------

    list_words = (
        "list",
        "show",
        "display",
        "available"
    )

    if (
        any(word in text.split() for word in list_words)
        and mentions_courses
    ):

        result = execute_tool("list_courses")

        if result["success"]:
            return (
                "Available courses:\n"
                + format_courses(result["result"])
            )

        return result["error"]

    # ---------------- SEARCH COURSES ----------------

    prefixes = [
        "please find ",
        "find ",
        "search for ",
        "look for ",
        "tell me about ",
        "describe ",
        "what is ",
        "show me ",
        "give me details about "
    ]

    query = text

    for prefix in prefixes:
        if query.startswith(prefix):
            query = query[len(prefix):].strip()
            break

    query = re.sub(
        r"^(?:the )?(?:course|subject)\s+",
        "",
        query
    )

    query = re.sub(
        r"\s+(?:course|subject)$",
        "",
        query
    ).strip(" ?.!")

    if query and query != text:

        result = execute_tool(
            "find_course",
            course_name=query
        )

        if not result["success"]:
            return result["error"]

        if result["result"]:
            return (
                "Matching courses:\n"
                + format_courses(result["result"])
            )

    # ---------------- UNKNOWN REQUEST ----------------

    return (
        "I couldn't confidently understand that request.\n"
        "Try asking about courses, course IDs, semesters, "
        "or summaries. Type 'help' for examples."
    )


# ==================================================
# 5. RUN THE AGENT
# ==================================================

if __name__ == "__main__":

    print("=" * 48)
    print("       AGENTIC AI COURSE MANAGEMENT")
    print("=" * 48)

    print("I can execute tools to retrieve course information.")
    print("Type 'help' for supported requests.")
    print("Type 'exit' to stop.")

    while True:

        try:
            user_input = input("\nYou: ").strip()

            if user_input.casefold() in {
                "exit",
                "quit",
                "bye"
            }:
                print("Agent: Goodbye!")
                break

            response = run_agent(user_input)

            print(f"\nAgent:\n{response}")

        except (KeyboardInterrupt, EOFError):
            print("\nAgent: Session ended.")
            break

