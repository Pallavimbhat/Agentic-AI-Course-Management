
"""
LAB 2: TOOL-USING AGENT

Tools:
1. Calculator
2. Course database operations
3. File reading and writing
4. HTTP API requests
"""

import ast
import json
import operator
import urllib.error
import urllib.request
from pathlib import Path


# ==================================================
# 1. CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)

COURSE_FILE = DATA_DIR / "courses.json"

DEFAULT_COURSES = [
    {
        "id": 1,
        "name": "Database Management Systems",
        "semester": 7
    },
    {
        "id": 2,
        "name": "Artificial Intelligence",
        "semester": 7
    },
    {
        "id": 3,
        "name": "Computer Networks",
        "semester": 6
    },
    {
        "id": 4,
        "name": "Machine Learning",
        "semester": 7
    },
    {
        "id": 5,
        "name": "Cloud Computing",
        "semester": 6
    }
]


def initialize_database():
    """Create the JSON course file if it doesn't exist."""

    if not COURSE_FILE.exists():
        COURSE_FILE.write_text(
            json.dumps(DEFAULT_COURSES, indent=4),
            encoding="utf-8"
        )


def load_courses():
    """Load course records from the JSON file."""

    initialize_database()

    return json.loads(
        COURSE_FILE.read_text(encoding="utf-8")
    )


# ==================================================
# 2. CALCULATOR TOOL
# ==================================================

BINARY_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def _evaluate_expression(node):
    """Evaluate only explicitly permitted arithmetic operations."""

    if isinstance(node, ast.Constant):
        if (
            isinstance(node.value, bool)
            or not isinstance(node.value, (int, float))
        ):
            raise ValueError("Only numeric values are allowed.")

        if abs(node.value) > 1_000_000_000:
            raise ValueError("Number is too large.")

        return node.value

    if isinstance(node, ast.BinOp):
        operation = BINARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported arithmetic operation.")

        left = _evaluate_expression(node.left)
        right = _evaluate_expression(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 10:
            raise ValueError("Exponent is too large.")

        result = operation(left, right)

        if abs(result) > 1e100:
            raise ValueError("Result is too large.")

        return result

    if isinstance(node, ast.UnaryOp):
        operation = UNARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Unsupported unary operation.")

        return operation(_evaluate_expression(node.operand))

    raise ValueError("Invalid arithmetic expression.")


def calculate(expression):
    """Safely calculate a basic arithmetic expression."""

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Provide an arithmetic expression.")

    if len(expression) > 200:
        raise ValueError("Expression is too long.")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate_expression(tree.body)

        return {
            "expression": expression,
            "result": result
        }

    except ZeroDivisionError:
        raise ValueError("Division by zero is not allowed.")

    except (SyntaxError, OverflowError):
        raise ValueError("Invalid arithmetic expression.")


# ==================================================
# 3. COURSE TOOLS
# ==================================================

def count_courses():
    """Count all stored courses."""

    return len(load_courses())


def list_courses():
    """Return all stored courses."""

    return load_courses()


def find_course(query):
    """Find courses using a partial name."""

    query = query.strip().casefold()

    if not query:
        return []

    return [
        course
        for course in load_courses()
        if query in course["name"].casefold()
    ]


def get_course_summary():
    """Return a summary of courses grouped by semester."""

    courses = load_courses()
    semester_counts = {}

    for course in courses:
        semester = course.get("semester", "Unknown")
        semester_counts[semester] = semester_counts.get(semester, 0) + 1

    return {
        "total_courses": len(courses),
        "semesters": semester_counts
    }

# ==================================================
# 4. FILE TOOLS
# ==================================================

def write_text_file(filename, content):
    """
    Write a text file inside the Lab 2 data directory.

    Arbitrary filesystem paths are not accepted.
    """

    safe_name = Path(filename).name

    if safe_name != filename or safe_name in {"", ".", ".."}:
        raise ValueError("Use a simple filename only.")

    if not safe_name.endswith(".txt"):
        raise ValueError("Only .txt files are allowed.")

    if not isinstance(content, str):
        raise ValueError("File content must be text.")

    if len(content) > 100_000:
        raise ValueError("File content is too large.")

    path = DATA_DIR / safe_name
    path.write_text(content, encoding="utf-8")

    return {
        "file": safe_name,
        "status": "created",
        "path": str(path)
    }


def read_text_file(filename):
    """Read a text file from the Lab 2 data directory."""

    safe_name = Path(filename).name

    if safe_name != filename or safe_name in {"", ".", ".."}:
        raise ValueError("Use a simple filename only.")

    if not safe_name.endswith(".txt"):
        raise ValueError("Only .txt files can be read.")

    path = DATA_DIR / safe_name

    if not path.is_file():
        raise FileNotFoundError(
            f"File '{safe_name}' does not exist."
        )

    return {
        "file": safe_name,
        "content": path.read_text(encoding="utf-8")
    }


def export_courses():
    """Export current courses to a text file."""

    courses = load_courses()

    content = "\n".join(
        f"{course['id']}. {course['name']} "
        f"(Semester {course['semester']})"
        for course in courses
    )

    return write_text_file("course_list.txt", content)


# ==================================================
# 5. HTTP API TOOL
# ==================================================

def call_api(url):
    """
    Make a GET request to an HTTP API.

    Only localhost URLs are allowed in this lab.
    Redirects are disabled to prevent requests to other hosts.
    """

    from urllib.parse import urlsplit
    from urllib.error import HTTPError

    parsed = urlsplit(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    if parsed.hostname not in {"127.0.0.1", "localhost"}:
        raise ValueError(
            "For this lab, API calls are restricted to localhost."
        )

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed.")

    if parsed.port not in {None, 8000}:
        raise ValueError("Only the configured local API port is allowed.")

    class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):
            return None

    opener = urllib.request.build_opener(NoRedirectHandler)

    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json"},
        method="GET"
    )

    try:
        with opener.open(request, timeout=5) as response:
            body = response.read(100_000).decode("utf-8")

            return {
                "status_code": response.status,
                "body": body
            }

    except HTTPError as error:
        return {
            "status_code": error.code,
            "body": "API returned an HTTP error."
        }

    except urllib.error.URLError:
        raise ConnectionError(
            "Could not connect to the local API. "
            "Make sure api_server.py is running."
        )


# ==================================================
# 6. INDEPENDENT TEST
# ==================================================

if __name__ == "__main__":

    print("=== LAB 2 TOOL TEST ===")

    print("\n1. Calculator:")
    print(calculate("25 * (4 + 2)"))

    print("\n2. Course count:")
    print(count_courses())

    print("\n3. Course list:")
    print(list_courses())

    print("\n4. Course search:")
    print(find_course("Artificial Intelligence"))

    print("\n5. Export courses:")
    print(export_courses())

    print("\n6. Read exported file:")
    print(read_text_file("course_list.txt"))

    print("\nAll basic tool tests completed.")
