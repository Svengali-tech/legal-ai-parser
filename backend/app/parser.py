from typing import List, Optional
from backend.app.analyzer import warrants


class Parser(warrants):
    name: str
    warrants: List[str]
    description: str


    def __init__(self, name: str, warrants: List[str], description: str) -> None:
        self.name = name
        self.warrants = warrants
        self.description = description


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None