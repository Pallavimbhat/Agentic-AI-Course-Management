"""Lab 5: Connector-based course management agent."""

from lab5.registry import ConnectorRegistry


registry = ConnectorRegistry()


def run_agent(user_message):
    text = " ".join(user_message.strip().split())
    message = text.casefold()

    if not message:
        return "Please enter a request."

    if message in {"exit", "quit", "bye"}:
        return "Goodbye!"

    if message in {"help", "commands"}:
        return """
LAB 5: CONNECTOR-BASED AGENT

Connectors:
  list connectors

SQLite:
  list database courses
  count database courses
  search database course Cloud Computing

Files:
  list files
  read file notes.txt
  write file notes.txt: Lab 5 completed

API:
  call api /health
  call api /courses
  call api /courses/count
  call api /courses/summary

Type exit to stop.
"""

    try:
        # Connector discovery
        if message in {"list connectors", "show connectors"}:
            return "\n".join(
                f"- {item['name']}: {item['description']}"
                for item in registry.list_connectors()
            )

        # SQLite operations
        sqlite = registry.get("sqlite")

        if message == "list database courses":
            return str(sqlite.list_courses())

        if message == "count database courses":
            return f"Database course count: {sqlite.count_courses()}"

        prefix = "search database course "

        if message.startswith(prefix):
            query = text[len(prefix):].strip()
            return str(sqlite.search_courses(query))

        # File operations
        file_connector = registry.get("file")

        if message == "list files":
            return str(file_connector.list_files())

        if message.startswith("read file "):
            filename = text[len("read file "):].strip()
            return str(file_connector.read_file(filename))

        if message.startswith("write file "):
            instruction = text[len("write file "):]

            if ":" not in instruction:
                return "Use: write file notes.txt: Your content"

            filename, content = instruction.split(":", 1)

            return str(
                file_connector.write_file(
                    filename.strip(),
                    content.strip(),
                )
            )

        # API operations
        api_connector = registry.get("api")

        if message.startswith("call api "):
            path = text[len("call api "):].strip()
            result = api_connector.get(path)
            return str(result)

        return (
            "I couldn't identify that operation. "
            "Type 'help' to see supported commands."
        )

    except (ValueError, KeyError, FileNotFoundError) as error:
        return f"Request error: {error}"

    except (ConnectionError, OSError) as error:
        return f"Connection or file error: {error}"


if __name__ == "__main__":
    print("=" * 48)
    print("LAB 5: CONNECTOR-BASED AGENT")
    print("=" * 48)
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