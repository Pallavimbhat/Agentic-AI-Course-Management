
import tempfile
import unittest
from pathlib import Path

from lab5.connectors.file_connector import FileConnector
from lab5.connectors.sqlite_connector import SQLiteConnector
from lab5.registry import ConnectorRegistry
from lab5.agent import run_agent


class TestFileConnector(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.connector = FileConnector()
        self.connector.data_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_write_and_read(self):
        self.connector.write_file("test.txt", "Hello Lab 5")
        result = self.connector.read_file("test.txt")
        self.assertEqual(result["content"], "Hello Lab 5")

    def test_reject_path_traversal(self):
        with self.assertRaises(ValueError):
            self.connector.read_file("../outside.txt")


class TestSQLiteConnector(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        # Create a connector without opening the real database.
        self.connector = SQLiteConnector.__new__(SQLiteConnector)

        # Use a temporary database for testing.
        self.connector.base_dir = Path(self.temp_dir.name)
        self.connector.data_dir = Path(self.temp_dir.name)
        self.connector.database_path = Path(self.temp_dir.name) / "test.db"

        self.connector.initialize_database()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_course_count(self):
        self.assertEqual(self.connector.count_courses(), 0)

    def test_search_empty_query(self):
        self.assertEqual(self.connector.search_courses(""), [])


class TestConnectorRegistry(unittest.TestCase):
    def test_registered_connectors(self):
        registry = ConnectorRegistry()
        names = {
            item["name"]
            for item in registry.list_connectors()
        }

        self.assertEqual(
            names,
            {"file_connector", "sqlite_connector", "api_connector"}
        )


class TestAgent(unittest.TestCase):
    def test_list_connectors(self):
        result = run_agent("list connectors")

        self.assertIn("file_connector", result)
        self.assertIn("sqlite_connector", result)
        self.assertIn("api_connector", result)

    def test_unknown_request(self):
        result = run_agent("do something unknown")
        self.assertIn("couldn't identify", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

