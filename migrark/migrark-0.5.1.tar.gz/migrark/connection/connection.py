from typing import Protocol, List, Dict, Sequence, Any


class Connection(Protocol):
    def open(self) -> None:
        """Open the database connection"""

    def close(self) -> None:
        """Close the database connection"""

    def execute(self, statement: str,
                parameters: Sequence[Any] = []) -> str:
        """Execute data modification commands"""

    def select(self, statement: str,
               parameters: Sequence[Any] = []) -> List[Dict[str, Any]]:
        """Select data from the database"""
