
"""SQLite connector for Lab 5."""

import json
import sqlite3
from pathlib import Path


class SQLiteConnector:
    name = "sqlite_connector"
    description = "Stores and queries course records using SQLite."

    def __init__(self):
        self.base_dir = Path(__file__).resolve().parents[1]
        self.data_dir = self.base_dir / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.database_path = self.data_dir / "courses.db"
        self.initialize_database()
        self.import_courses()

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def initialize_database(self):
        connection = self._connect()
        try:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    semester INTEGER NOT NULL
                )
            """)
            connection.commit()
        finally:
            connection.close()

    def import_courses(self):
        source_file = self.base_dir.parent / "lab2" / "data" / "courses.json"

        if not source_file.exists():
            return {
                "imported": 0,
                "message": "Lab 2 course JSON file was not found."
            }

        try:
            courses = json.loads(source_file.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise ValueError(
                f"Could not read Lab 2 course data: {error}"
            ) from error

        connection = self._connect()
        imported = 0

        try:
            for course in courses:
                cursor = connection.execute(
                    """
                    INSERT OR IGNORE INTO courses (id, name, semester)
                    VALUES (?, ?, ?)
                    """,
                    (
                        course["id"],
                        course["name"],
                        course["semester"],
                    ),
                )
                imported += cursor.rowcount

            connection.commit()
        finally:
            connection.close()

        return {
            "imported": imported,
            "message": "Course import completed."
        }

    def list_courses(self):
        connection = self._connect()
        try:
            rows = connection.execute(
                "SELECT id, name, semester FROM courses ORDER BY id"
            ).fetchall()

            return [
                {"id": row[0], "name": row[1], "semester": row[2]}
                for row in rows
            ]
        finally:
            connection.close()

    def count_courses(self):
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT COUNT(*) FROM courses"
            ).fetchone()
            return row[0]
        finally:
            connection.close()

    def search_courses(self, query):
        if not isinstance(query, str) or not query.strip():
            return []

        connection = self._connect()
        try:
            rows = connection.execute(
                """
                SELECT id, name, semester
                FROM courses
                WHERE name LIKE ? COLLATE NOCASE
                ORDER BY id
                """,
                (f"%{query.strip()}%",),
            ).fetchall()

            return [
                {"id": row[0], "name": row[1], "semester": row[2]}
                for row in rows
            ]
        finally:
            connection.close()
