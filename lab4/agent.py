
"""
LAB 4: MEMORY-ENABLED COURSE MANAGEMENT AGENT

Supports:
- Short-term memory
- Long-term memory
- Memory retrieval
- Memory status
"""

from lab4.memory import MemorySystem


# =====================================================
# 1. INITIALIZE MEMORY
# =====================================================

memory = MemorySystem()


# =====================================================
# 2. REQUEST ROUTER
# =====================================================

def run_agent(user_message):
    """Route user requests to memory operations."""

    text = " ".join(user_message.strip().split())
    message = text.casefold()

    if not message:
        return "Please enter a request."

    if message in {"exit", "quit", "bye"}:
        return "Goodbye!"

    if message in {"help", "commands"}:
        return """
LAB 4: MEMORY AND RETRIEVAL

Remember for this session:
  remember short: I am studying Cloud Computing

Save permanently:
  remember long: I want to learn Artificial Intelligence

Retrieve memories:
  recall short
  recall long
  recall Cloud Computing
  search memory Artificial Intelligence

Memory status:
  memory status

Type exit to stop.
"""

    # -------------------------------------------------
    # SHORT-TERM MEMORY STORAGE
    # -------------------------------------------------

    if message.startswith("remember short:"):
        content = text.split(":", 1)[1].strip()

        try:
            entry = memory.remember_short_term(content)

            return f"Remembered for this session: {entry['text']}"

        except ValueError as error:
            return f"Memory error: {error}"

    # -------------------------------------------------
    # LONG-TERM MEMORY STORAGE
    # -------------------------------------------------

    if message.startswith("remember long:"):
        content = text.split(":", 1)[1].strip()

        try:
            entry = memory.remember_long_term(content)

            return f"Saved permanently: {entry['text']}"

        except (ValueError, OSError) as error:
            return f"Memory error: {error}"

    # -------------------------------------------------
    # RETRIEVE SHORT-TERM MEMORY
    # -------------------------------------------------

    if message == "recall short":
        entries = memory.retrieve_short_term()

        if not entries:
            return "No short-term memories in this session."

        return "Short-term memories:\n" + "\n".join(
            f"- {entry['text']}" for entry in entries
        )

    # -------------------------------------------------
    # RETRIEVE LONG-TERM MEMORY
    # -------------------------------------------------

    if message == "recall long":
        entries = memory.retrieve_long_term()

        if not entries:
            return "No long-term memories have been saved."

        return "Long-term memories:\n" + "\n".join(
            f"- {entry['text']}" for entry in entries
        )

    # -------------------------------------------------
    # SEARCH MEMORY
    # -------------------------------------------------

    if message.startswith("search memory "):
        query = text[len("search memory "):].strip()
        results = memory.retrieve(query)

        lines = []

        for entry in results["short_term"]:
            lines.append(f"[Short-term] {entry['text']}")

        for entry in results["long_term"]:
            lines.append(f"[Long-term] {entry['text']}")

        if not lines:
            return f"No memories found matching '{query}'."

        return "Matching memories:\n" + "\n".join(lines)

    # -------------------------------------------------
    # RECALL BY QUERY
    # -------------------------------------------------

    if message.startswith("recall "):
        query = text[len("recall "):].strip()
        results = memory.retrieve(query)

        lines = []

        for entry in results["short_term"]:
            lines.append(f"[Short-term] {entry['text']}")

        for entry in results["long_term"]:
            lines.append(f"[Long-term] {entry['text']}")

        if not lines:
            return f"No memories found matching '{query}'."

        return "Retrieved memories:\n" + "\n".join(lines)

    # -------------------------------------------------
    # MEMORY STATUS
    # -------------------------------------------------

    if message == "memory status":
        result = memory.status()

        return (
            f"Short-term memories: {result['short_term_count']}\n"
            f"Long-term memories: {result['long_term_count']}\n"
            f"Persistent storage: {result['storage_file']}"
        )

    return (
        "I couldn't identify the requested operation.\n"
        "Type 'help' to see supported commands."
    )


# =====================================================
# 3. INTERACTIVE LOOP
# =====================================================

if __name__ == "__main__":

    print("=" * 50)
    print("LAB 4: MEMORY AND RETRIEVAL AGENT")
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

