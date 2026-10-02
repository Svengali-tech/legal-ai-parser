from backend.app.parser import Parser
from backend.app.analyzer import warrants
from typing import List
from fastapi import UploadFile, File

forms = {
    "name": "NYPD Arrest Warrant",
    "warrants": ["warrant1", "warrant2"]
}


def analyze(forms: dict) -> Parser:
    return Parser(
        name=forms["name"],
        warrants=forms["warrant 1"],
        description="string"
    )

def analyze(forms: dict) -> Parser:
    return Parser(
        name=forms["name"],
        warrants=forms["warrant 2"],
        description="string"
    )
