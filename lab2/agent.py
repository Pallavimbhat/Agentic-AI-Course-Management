
"""
LAB 2: TOOL-USING COURSE MANAGEMENT AGENT

Tools:
1. Calculator
2. Course database operations
3. File reading and writing
4. HTTP API requests

This is a rule-based agent that routes requests to registered tools.
"""

import re

from lab2.tools import (
    calculate,
    count_courses,
    list_courses,
    find_course,
    read_text_file,
    write_text_file,
    export_courses,
    call_api,
)


# ============================================================
# 1. TOOL REGISTRY
# ============================================================

TOOLS = {
    "calculate": calculate,
    "count_courses": count_courses,
    "list_courses": list_courses,
    "find_course": find_course,
    "read_text_file": read_text_file,
    "write_text_file": write_text_file,
    "export_courses": export_courses,
    "call_api": call_api,
}


# ============================================================
# 2. RESPONSE FORMATTERS
# ============================================================

def format_courses(courses):
    """Format a list of course records for display."""

    if not courses:
        return "No matching courses found."

    return "\n".join(
        f"- {course['name']} "
        f"(ID {course['id']}, Semester {course['semester']})"
        for course in courses
    )


# ============================================================
# 3. TOOL EXECUTION
# ============================================================

def execute_tool(name, **kwargs):
    """Find and execute a registered tool."""

    tool = TOOLS.get(name)

    if tool is None:
        return {
            "success": False,
            "error": f"Unknown tool: {name}"
        }

    try:
        result = tool(**kwargs)

        return {
            "success": True,
            "result": result
        }

    except (
        ValueError,
        TypeError,
        FileNotFoundError,
        ConnectionError,
    ) as error:
        return {
            "success": False,
            "error": str(error)
        }

    except Exception as error:
        return {
            "success": False,
            "error": f"Unexpected tool error: {error}"
        }


# ============================================================
# 4. REQUEST ROUTER
# ============================================================

def run_agent(user_message):
    """
    Identify the user's request and route it to the correct tool.
    """

    text = " ".join(user_message.strip().split())
    message = text.casefold()

    if not message:
        return "Please enter a request."

    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    if message in {"exit", "quit", "bye"}:
        return "Goodbye!"

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if message in {
        "help",
        "commands",
        "what can you do",
        "show help",
    }:
        return """
================================================
LAB 2: TOOL-USING AGENT
================================================

CALCULATOR
  calculate 25 * (4 + 2)
  calculate 100 / 4

COURSE OPERATIONS
  count courses
  how many courses are there
  list courses
  show all courses
  find course Cloud Computing
  find the course Cloud Computing
  search course Artificial Intelligence

FILE OPERATIONS
  export courses
  read file course_list.txt
  write file notes.txt: Lab 2 completed

API OPERATIONS
  check API
  call API /health
  call API /courses
  call API /courses/count
  call_api /courses/count

TOOLS
  list tools
  show tools

Type 'exit' to stop.
================================================
"""

    # --------------------------------------------------------
    # LIST REGISTERED TOOLS
    # --------------------------------------------------------

    if message in {
        "list tools",
        "show tools",
        "available tools",
        "list_tools",
    }:
        return (
            "Available tools:\n"
            + "\n".join(f"- {name}" for name in TOOLS)
        )

    # --------------------------------------------------------
    # CALCULATOR
    # --------------------------------------------------------

    if message.startswith("calculate "):
        expression = text[len("calculate "):].strip()

        result = execute_tool(
            "calculate",
            expression=expression,
        )

        if result["success"]:
            return f"Result: {result['result']['result']}"

        return f"Calculation error: {result['error']}"

    # --------------------------------------------------------
    # COUNT COURSES
    # --------------------------------------------------------

    count_patterns = [
        r"count[_ ]courses?",
        r"count[_ ]subjects?",
        r"how many courses?(?: are there)?",
        r"how many subjects?(?: are there)?",
        r"total number of courses?",
        r"total courses?",
    ]

    if any(re.search(pattern, message) for pattern in count_patterns):
        result = execute_tool("count_courses")

        if result["success"]:
            return f"Total courses: {result['result']}"

        return f"Course error: {result['error']}"

    # --------------------------------------------------------
    # LIST COURSES
    # --------------------------------------------------------

    list_commands = {
        "list courses",
        "list course",
        "list_courses",
        "show courses",
        "show course",
        "show all courses",
        "display courses",
        "display course",
        "show all subjects",
    }

    if message in list_commands:
        result = execute_tool("list_courses")

        if result["success"]:
            return format_courses(result["result"])

        return f"Course error: {result['error']}"

    # --------------------------------------------------------
    # SEARCH FOR A COURSE
    # --------------------------------------------------------

    search_match = re.match(
        r"^(?:find|search)\s+"
        r"(?:the\s+)?"
        r"(?:course|courses|subject|subjects)\s+"
        r"(.+)$",
        text,
        flags=re.IGNORECASE,
    )

    if search_match:
        query = search_match.group(1).strip()

        result = execute_tool(
            "find_course",
            query=query,
        )

        if result["success"]:
            return format_courses(result["result"])

        return f"Course search error: {result['error']}"

    # --------------------------------------------------------
    # EXPORT COURSES
    # --------------------------------------------------------

    if message in {
        "export courses",
        "export course",
        "export_courses",
        "save course list",
        "save courses",
    }:
        result = execute_tool("export_courses")

        if result["success"]:
            return (
                "Course list exported successfully to "
                f"{result['result']['file']}."
            )

        return f"Export error: {result['error']}"

    # --------------------------------------------------------
    # READ A TEXT FILE
    # --------------------------------------------------------

    read_match = re.match(
        r"^(?:read file|read_text_file)\s+(.+)$",
        text,
        flags=re.IGNORECASE,
    )

    if read_match:
        filename = read_match.group(1).strip()

        result = execute_tool(
            "read_text_file",
            filename=filename,
        )

        if result["success"]:
            return result["result"]["content"]

        return f"File error: {result['error']}"

    # --------------------------------------------------------
    # WRITE A TEXT FILE
    # --------------------------------------------------------

    if message.startswith("write file "):
        match = re.fullmatch(
            r"write file ([^:]+):\s*(.*)",
            text,
            flags=re.DOTALL | re.IGNORECASE,
        )

        if not match:
            return (
                "Incorrect format.\n"
                "Use: write file notes.txt: Your text here"
            )

        filename = match.group(1).strip()
        content = match.group(2)

        result = execute_tool(
            "write_text_file",
            filename=filename,
            content=content,
        )

        if result["success"]:
            return (
                "File created successfully: "
                f"{result['result']['file']}"
            )

        return f"File error: {result['error']}"

    # --------------------------------------------------------
    # CHECK OR CALL THE LOCAL API
    # --------------------------------------------------------

    path = None

    if message in {"check api", "check_api"}:
        path = "/health"

    elif message.startswith("call api "):
        path = text[len("call api "):].strip()

    elif message.startswith("call_api "):
        path = text[len("call_api "):].strip()

    if path is not None:

        # Only API paths are accepted, not arbitrary URLs.
        if not path.startswith("/") or path.startswith("//"):
            return (
                "Provide an API path beginning with one slash.\n"
                "Example: call API /courses/count"
            )

        if "://" in path:
            return (
                "Provide an API path, not a complete URL.\n"
                "Example: call API /courses/count"
            )

        result = execute_tool(
            "call_api",
            url="http://127.0.0.1:8000" + path,
        )

        if result["success"]:
            return (
                f"HTTP status: {result['result']['status_code']}\n"
                f"Response: {result['result']['body']}"
            )

        return f"API error: {result['error']}"

    # --------------------------------------------------------
    # UNKNOWN REQUEST
    # --------------------------------------------------------

    return (
        "I couldn't identify the requested operation.\n"
        "Type 'help' to see supported commands."
    )


# ============================================================
# 5. INTERACTIVE LOOP
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("       LAB 2: TOOL-USING AGENT")
    print("=" * 50)

    print("This agent uses registered Python tools.")
    print("Type 'help' for examples.")
    print("Type 'exit' to stop.")

    while True:
        try:
            user_input = input("\nYou: ")

            response = run_agent(user_input)

            print("\nAgent:", response)

            if user_input.strip().casefold() in {
                "exit",
                "quit",
                "bye",
            }:
                break

        except (KeyboardInterrupt, EOFError):
            print("\nAgent: Session ended.")
            break

