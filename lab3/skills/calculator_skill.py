"""
LAB 3: CALCULATOR SKILL

A reusable skill for mathematical calculations.
"""

from lab2.tools import calculate


class CalculatorSkill:
    """Reusable calculator capability."""

    name = "calculator"

    description = (
        "Evaluates arithmetic expressions using the existing "
        "Lab 2 calculator tool."
    )

    instructions = [
        "Accept a mathematical expression.",
        "Pass the expression to the calculate tool.",
        "Return the calculated result.",
    ]

    def execute(self, expression):
        """Calculate the supplied expression."""

        if not expression or not expression.strip():
            return {
                "error": "Provide a mathematical expression."
            }

        try:
            return calculate(expression)

        except (ValueError, TypeError) as error:
            return {
                "error": str(error)
            }