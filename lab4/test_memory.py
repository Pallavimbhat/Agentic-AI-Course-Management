
"""
Tests for Lab 4 memory and retrieval.
"""

import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch

from lab4.memory import MemorySystem
from lab4.agent import run_agent


class TestMemorySystem(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.memory_file = Path(self.temp_dir.name) / "memory.json"

        self.file_patcher = patch(
            "lab4.memory.MEMORY_FILE",
            self.memory_file
        )
        self.file_patcher.start()

        self.memory = MemorySystem()

    def tearDown(self):
        self.file_patcher.stop()
        self.temp_dir.cleanup()

    def test_short_term_memory(self):
        self.memory.remember_short_term(
            "I am studying Cloud Computing"
        )

        results = self.memory.retrieve_short_term("Cloud Computing")

        self.assertEqual(len(results), 1)

    def test_long_term_memory(self):
        self.memory.remember_long_term(
            "I want to learn Artificial Intelligence"
        )

        results = self.memory.retrieve_long_term("Artificial Intelligence")

        self.assertEqual(len(results), 1)

    def test_long_term_persistence(self):
        self.memory.remember_long_term("Remember this information")

        second_instance = MemorySystem()

        results = second_instance.retrieve_long_term("information")

        self.assertEqual(len(results), 1)

    def test_combined_retrieval(self):
        self.memory.remember_short_term("Studying Python")
        self.memory.remember_long_term("Learning Python")

        results = self.memory.retrieve("Python")

        self.assertEqual(len(results["short_term"]), 1)
        self.assertEqual(len(results["long_term"]), 1)

    def test_empty_memory_rejected(self):
        with self.assertRaises(ValueError):
            self.memory.remember_long_term("   ")


class TestMemoryAgent(unittest.TestCase):

    def test_short_term_command(self):
        result = run_agent(
            "remember short: Testing memory"
        )

        self.assertIn("Remembered", result)

    def test_long_term_command(self):
        result = run_agent(
            "remember long: Testing persistent memory"
        )

        self.assertIn("Saved permanently", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

