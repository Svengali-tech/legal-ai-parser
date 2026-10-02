from pydantic import BaseModel, Field
from typing import List
from backend.app.models import User, Post

class Parser(warrants):
    warrants: List[str] = Field(description="List of legal warranties extracted from the contract.")
    if 


    class Config:
        orm_mode = True

    def __init__(self, warrants: List[str]):
        self.warrants = warrants

        super().__init__()