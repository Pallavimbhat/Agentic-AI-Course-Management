
"""
LAB 1: AGENT VS CHATBOT
Basic Course Management Chatbot

This chatbot provides general conversational responses.
It does not call tools or retrieve course records.
"""


# ==================================================
# 1. CHATBOT RESPONSE LOGIC
# ==================================================

def chatbot_response(user_message):

    message = " ".join(user_message.strip().split()).casefold()

    if not message:
        return "Please enter a message."

    # Greetings
    if message in {
        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    }:
        return (
            "Hello! Welcome to the Course Management System. "
            "How can I help you?"
        )

    # Identity
    if message in {
        "who are you",
        "what are you"
    }:
        return (
            "I am a basic Course Management Chatbot. "
            "I answer general questions about academic management."
        )

    # Help
    if message in {
        "help",
        "what can you do",
        "what can you help me with"
    }:
        return (
            "I can explain courses, notes, assignments, "
            "and submissions. I cannot retrieve live course records."
        )

    # General course questions
    if "course" in message or "subject" in message:
        return (
            "A course is a structured academic subject containing "
            "learning objectives, topics, and study materials. "
            "I cannot query actual course records."
        )

    # Assignment questions
    if "assignment" in message:
        return (
            "An assignment is an academic task given to students. "
            "It may include instructions, a deadline, and evaluation criteria."
        )

    # Notes questions
    if "notes" in message:
        return (
            "Course notes contain learning materials that help "
            "students understand their subjects."
        )

    # Submission questions
    if "submission" in message:
        return (
            "A submission is work handed in by a student "
            "for an assignment or assessment."
        )

    # Thanks
    if "thank" in message:
        return "You're welcome! Feel free to ask another question."

    # Default response
    return (
        "I can answer general questions about course management. "
        "Try asking about courses, notes, assignments, or submissions."
    )


# ==================================================
# 2. RUN THE CHATBOT
# ==================================================

if __name__ == "__main__":

    print("=" * 48)
    print("       BASIC COURSE MANAGEMENT CHATBOT")
    print("=" * 48)

    print("I can answer general academic questions.")
    print("Type 'help' for examples.")
    print("Type 'exit' to stop.")

    while True:

        try:
            user_input = input("\nYou: ").strip()

            if user_input.casefold() in {
                "exit",
                "quit",
                "bye"
            }:
                print("Chatbot: Goodbye!")
                break

            response = chatbot_response(user_input)

            print(f"\nChatbot: {response}")

        except (KeyboardInterrupt, EOFError):
            print("\nChatbot: Session ended.")
            break

