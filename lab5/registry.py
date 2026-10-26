"""Registry for Lab 5 connectors."""

from lab5.connectors import (
    FileConnector,
    SQLiteConnector,
    APIConnector,
)


class ConnectorRegistry:
    """Register connectors and expose their capabilities."""

    def __init__(self):
        self.connectors = {
            "file": FileConnector(),
            "sqlite": SQLiteConnector(),
            "api": APIConnector(),
        }

    def get(self, name):
        """Retrieve a connector by name."""

        if name not in self.connectors:
            raise KeyError(f"Unknown connector: {name}")

        return self.connectors[name]

    def list_connectors(self):
        """Describe registered connectors."""

        return [
            {
                "name": connector.name,
                "description": connector.description,
            }
            for connector in self.connectors.values()
        ]