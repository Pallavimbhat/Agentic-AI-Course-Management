"""
LAB 3: FILE MANAGEMENT SKILL

A reusable skill for reading, writing, and exporting course files.
"""

from lab2.tools import (
    read_text_file,
    write_text_file,
    export_courses,
)


class FileManagementSkill:
    """Reusable file-management capability."""

    name = "file_management"

    description = (
        "Reads text files, writes text files, "
        "and exports the course list."
    )

    instructions = [
        "Use read to read an existing text file.",
        "Use write to save text to a file.",
        "Use export_courses to export the course list.",
        "Use only the safe file operations provided by the tools.",
    ]

    def execute(self, action, filename=None, content=None):
        """Execute a file-management operation."""

        if action == "read":
            if not filename:
                return {
                    "error": "Provide a filename to read."
                }

            try:
                return read_text_file(filename)

            except (ValueError, FileNotFoundError) as error:
                return {
                    "error": str(error)
                }

        if action == "write":
            if not filename:
                return {
                    "error": "Provide a filename to write."
                }

            if content is None:
                return {
                    "error": "Provide content to write."
                }

            try:
                return write_text_file(filename, content)

            except (ValueError, TypeError) as error:
                return {
                    "error": str(error)
                }

        if action == "export":
            try:
                return export_courses()

            except (ValueError, TypeError, OSError) as error:
                return {
                    "error": str(error)
                }

        return {
            "error": f"Unsupported file action: {action}"
        }