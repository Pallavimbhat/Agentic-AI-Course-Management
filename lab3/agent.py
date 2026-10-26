"""
LAB 3: SKILL-BASED COURSE MANAGEMENT AGENT

The agent routes user requests to reusable skill modules.
"""

from lab3.skills import (
    CourseManagementSkill,
    CalculatorSkill,
    FileManagementSkill,
)


# =====================================================
# 1. SKILL REGISTRY
# =====================================================

SKILLS = {
    "course_management": CourseManagementSkill(),
    "calculator": CalculatorSkill(),
    "file_management": FileManagementSkill(),
}


# =====================================================
# 2. SKILL EXECUTION
# =====================================================

def execute_skill(skill_name, **kwargs):
    """Find a registered skill and execute it."""

    skill = SKILLS.get(skill_name)

    if skill is None:
        return {
            "success": False,
            "error": f"Unknown skill: {skill_name}",
        }

    try:
        result = skill.execute(**kwargs)

        if isinstance(result, dict) and "error" in result:
            return {
                "success": False,
                "error": result["error"],
            }

        return {
            "success": True,
            "result": result,
        }

    except Exception as error:
        return {
            "success": False,
            "error": str(error),
        }


# =====================================================
# 3. REQUEST ROUTER
# =====================================================

def run_agent(user_message):
    """Route a user request to a reusable skill."""

    text = " ".join(user_message.strip().split())
    message = text.casefold()

    if not message:
        return "Please enter a request."

    if message in {"exit", "quit", "bye"}:
        return "Goodbye!"

    if message in {"help", "commands"}:
        return """
LAB 3: SKILL-BASED AGENT

Courses:
  list courses
  count courses
  find course Cloud Computing
  course summary

Calculator:
  calculate 25 * (4 + 2)

Files:
  export courses
  read file course_list.txt
  write file notes.txt: Lab 3 completed

Skills:
  list skills

Type exit to stop.
"""

    # List registered skills
    if message in {"list skills", "show skills"}:
        return "Registered skills:\n" + "\n".join(
            f"- {name}: {skill.description}"
            for name, skill in SKILLS.items()
        )

    # Calculator skill
    if message.startswith("calculate "):
        expression = text[len("calculate "):].strip()

        result = execute_skill(
            "calculator",
            expression=expression,
        )

        if result["success"]:
            return f"Calculation result: {result['result']['result']}"

        return f"Calculator error: {result['error']}"

    # Count courses
    if message in {"count courses", "count course"}:
        result = execute_skill(
            "course_management",
            action="count",
        )

        if result["success"]:
            return (
                "Total courses: "
                f"{result['result']['total_courses']}"
            )

        return f"Course error: {result['error']}"

    # List courses
    if message in {"list courses", "show courses"}:
        result = execute_skill(
            "course_management",
            action="list",
        )

        if result["success"]:
            courses = result["result"]

            if not courses:
                return "No courses are available."

            return "\n".join(
                f"- {course['name']} "
                f"(ID {course['id']}, Semester {course['semester']})"
                for course in courses
            )

        return f"Course error: {result['error']}"

    # Search courses
    if message.startswith("find course "):
        query = text[len("find course "):].strip()

        result = execute_skill(
            "course_management",
            action="search",
            query=query,
        )

        if not result["success"]:
            return f"Course search error: {result['error']}"

        courses = result["result"]

        if not courses:
            return "No matching courses found."

        return "\n".join(
            f"- {course['name']} "
            f"(ID {course['id']}, Semester {course['semester']})"
            for course in courses
        )

    # Course summary
    if message in {"course summary", "summarize courses"}:
        result = execute_skill(
            "course_management",
            action="summary",
        )

        if result["success"]:
            return f"Course summary: {result['result']}"

        return f"Course error: {result['error']}"

    # Export courses
    if message == "export courses":
        result = execute_skill(
            "file_management",
            action="export",
        )

        if result["success"]:
            return (
                "Courses exported successfully. "
                f"File: {result['result']['file']}"
            )

        return f"File error: {result['error']}"

    # Read a text file
    if message.startswith("read file "):
        filename = text[len("read file "):].strip()

        result = execute_skill(
            "file_management",
            action="read",
            filename=filename,
        )

        if result["success"]:
            return result["result"]["content"]

        return f"File error: {result['error']}"

    # Write a text file
    if message.startswith("write file "):
        instruction = text[len("write file "):]

        if ":" not in instruction:
            return (
                "Use this format: "
                "write file notes.txt: Your text here"
            )

        filename, content = instruction.split(":", 1)

        result = execute_skill(
            "file_management",
            action="write",
            filename=filename.strip(),
            content=content.strip(),
        )

        if result["success"]:
            return (
                "File created successfully: "
                f"{result['result']['file']}"
            )

        return f"File error: {result['error']}"

    return (
        "I couldn't identify the requested operation. "
        "Type 'help' to see supported commands."
    )


# =====================================================
# 4. INTERACTIVE LOOP
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print("LAB 3: SKILL CREATION AGENT")
    print("=" * 50)

    print("Type 'help' for commands.")
    print("Type 'exit' to stop.")

    while True:
        try:
            user_input = input("\nYou: ")
            response = run_agent(user_input)

            print("\nAgent:", response)

            if user_input.strip().casefold() in {
                "exit", "quit", "bye"
            }:
                break

        except (KeyboardInterrupt, EOFError):
            print("\nAgent: Session ended.")
            break