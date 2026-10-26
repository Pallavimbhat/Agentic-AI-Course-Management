"""
Tests for Lab 3 reusable skills.
"""

import unittest

from lab3.skills import (
    CourseManagementSkill,
    CalculatorSkill,
    FileManagementSkill,
)
from lab3.agent import run_agent


class TestCourseManagementSkill(unittest.TestCase):

    def setUp(self):
        self.skill = CourseManagementSkill()

    def test_count_courses(self):
        result = self.skill.execute("count")
        self.assertGreaterEqual(result["total_courses"], 0)

    def test_list_courses(self):
        result = self.skill.execute("list")
        self.assertIsInstance(result, list)

    def test_search_course(self):
        result = self.skill.execute(
            "search",
            query="Cloud Computing",
        )
        self.assertTrue(
            any(
                "Cloud Computing" in course["name"]
                for course in result
            )
        )


class TestCalculatorSkill(unittest.TestCase):

    def setUp(self):
        self.skill = CalculatorSkill()

    def test_calculation(self):
        result = self.skill.execute("25 * (4 + 2)")
        self.assertEqual(result["result"], 150)


class TestFileManagementSkill(unittest.TestCase):

    def setUp(self):
        self.skill = FileManagementSkill()

    def test_export_courses(self):
        result = self.skill.execute("export")
        self.assertIn("file", result)


class TestAgent(unittest.TestCase):

    def test_calculator_routing(self):
        result = run_agent("calculate 10 + 5")
        self.assertIn("15", result)

    def test_skill_listing(self):
        result = run_agent("list skills")
        self.assertIn("course_management", result)
        self.assertIn("calculator", result)
        self.assertIn("file_management", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)