
"""
LAB 4: MEMORY AND RETRIEVAL

Implements:
1. Short-term memory for the current session.
2. Long-term memory stored in a JSON file.
3. Retrieval of previously stored information.
"""

import json
from datetime import datetime, timezone
from pathlib import Path


# =====================================================
# 1. CONFIGURATION
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
MEMORY_DIR = BASE_DIR / "data"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

MEMORY_FILE = MEMORY_DIR / "long_term_memory.json"


# =====================================================
# 2. MEMORY CLASS
# =====================================================

class MemorySystem:
    """Manage short-term and persistent long-term memory."""

    def __init__(self):
        # Short-term memory exists only during this session.
        self.short_term_memory = []

        # Long-term memory is loaded from disk.
        self.long_term_memory = self._load_long_term_memory()

    # -------------------------------------------------
    # LONG-TERM MEMORY STORAGE
    # -------------------------------------------------

    def _load_long_term_memory(self):
        """Load saved memories from JSON."""

        if not MEMORY_FILE.exists():
            return []

        try:
            data = json.loads(
                MEMORY_FILE.read_text(encoding="utf-8")
            )

            if isinstance(data, list):
                return data

            return []

        except (json.JSONDecodeError, OSError):
            return []

    def _save_long_term_memory(self):
        """Persist long-term memories to JSON."""

        temporary_file = MEMORY_FILE.with_suffix(".tmp")

        temporary_file.write_text(
            json.dumps(
                self.long_term_memory,
                indent=4,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        temporary_file.replace(MEMORY_FILE)

    # -------------------------------------------------
    # SHORT-TERM MEMORY
    # -------------------------------------------------

    def remember_short_term(self, text):
        """Remember information until this instance ends."""

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Memory text cannot be empty.")

        entry = {
            "text": text.strip(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.short_term_memory.append(entry)

        return entry

    def retrieve_short_term(self, query=None):
        """Retrieve recent session memories."""

        if not query:
            return list(reversed(self.short_term_memory))

        query_words = set(query.casefold().split())

        matches = []

        for entry in reversed(self.short_term_memory):
            text_words = set(entry["text"].casefold().split())

            if query_words.intersection(text_words):
                matches.append(entry)

        return matches

    # -------------------------------------------------
    # LONG-TERM MEMORY
    # -------------------------------------------------

    def remember_long_term(self, text):
        """Save information so it survives program restarts."""

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Memory text cannot be empty.")

        entry = {
            "id": len(self.long_term_memory) + 1,
            "text": text.strip(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        self.long_term_memory.append(entry)
        self._save_long_term_memory()

        return entry

    def retrieve_long_term(self, query=None):
        """Search saved memories using case-insensitive text matching."""

        if not query:
            return list(reversed(self.long_term_memory))

        query_words = set(query.casefold().split())

        matches = []

        for entry in reversed(self.long_term_memory):
            text_words = set(entry["text"].casefold().split())

            if query_words.intersection(text_words):
                matches.append(entry)

        return matches

    # -------------------------------------------------
    # GENERAL RETRIEVAL
    # -------------------------------------------------

    def retrieve(self, query):
        """Search both memory types."""

        return {
            "short_term": self.retrieve_short_term(query),
            "long_term": self.retrieve_long_term(query)
        }

    # -------------------------------------------------
    # MEMORY STATUS
    # -------------------------------------------------

    def status(self):
        """Return the number of stored memories."""

        return {
            "short_term_count": len(self.short_term_memory),
            "long_term_count": len(self.long_term_memory),
            "storage_file": str(MEMORY_FILE)
        }

