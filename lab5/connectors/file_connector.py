"""File connector for Lab 5."""

from pathlib import Path


class FileConnector:
    name = "file_connector"

    description = "Reads and writes text files in the Lab 5 data directory."

    def __init__(self):
        self.data_dir = Path(__file__).resolve().parents[1] / "data"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, filename):
        """Validate a simple filename and return its path."""

        if not isinstance(filename, str):
            raise ValueError("Filename must be text.")

        if (
            not filename
            or Path(filename).name != filename
            or filename in {".", ".."}
            or not filename.endswith(".txt")
        ):
            raise ValueError("Use a simple .txt filename only.")

        return self.data_dir / filename

    def read_file(self, filename):
        """Read an existing text file."""

        path = self._get_path(filename)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {filename}")

        return {
            "filename": filename,
            "content": path.read_text(encoding="utf-8"),
        }

    def write_file(self, filename, content):
        """Create or update a text file."""

        if not isinstance(content, str):
            raise ValueError("Content must be text.")

        if len(content) > 100_000:
            raise ValueError("Content is too large.")

        path = self._get_path(filename)
        path.write_text(content, encoding="utf-8")

        return {
            "filename": filename,
            "status": "written",
        }

    def list_files(self):
        """List available text files."""

        return sorted(
            path.name
            for path in self.data_dir.glob("*.txt")
            if path.is_file()
        )