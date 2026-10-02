from typing import List
from backend.app.analyzer import warrants


class Parser(warrants):
    name: str
    warrants: List[str]
    description: str


    def __init__(self, name: str, warrants: List[str], description: str) -> None:
        self.name = name
        self.warrants = warrants
        self.description = description