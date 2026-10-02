from fastapi import FastAPI, File
from uvicorn import run
from fastapi import UploadFile
from backend.app.analyzer import analyze
from backend.app.parser import Parser
from typing import List
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import pymupdf
from starlette.concurrency import run_in_threadpool

app = FastAPI(title="legal-ai-parser")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Default fallback values
    status_code = 500
    message = "An error occurred during the request."

    # This is the "switch" statement checking the type of error raised
    match exc:
        case HTTPException() as http_exc:
            # Captures 200, 400, 401, 403, 404, etc., if they were raised as an HTTPException
            status_code = http_exc.status_code
            message = http_exc.detail

        case ValueError():
            # Turns a ValueError into a 400 Bad Request
            status_code = 400
            message = f"Invalid input value: {str(exc)}"

        case KeyError():
            # Turns a missing dictionary key error into a 404 Not Found
            status_code = 404
            message = f"Requested item or attribute not found: {str(exc)}"

        case _:
            # Fallback for any unmapped 500 Internal Server Errors
            message = f"Unexpected system error: {str(exc)}"

    return JSONResponse(
        status_code=status_code,
        headers={"WWW-Authenticate": "Bearer"},
        content={"message": message}
    )

app.add_api_route("/health", lambda: {"status": "healthy"}, methods=["GET, POST, PUT, DELETE, OPTIONS, HEAD, PATCH, TRACE"])



Run: uvicorn main:app --host 0.0.0.0 --port 8000


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/upload")
async def create_upload_file(my_file: UploadFile = File(official_warrant: str)):
    return {"filename": my_file.filename, "official_warrant": official_warrant}

@app.post("/api/analyze")
async def analyze(
    file_v1: UploadFile = File(...),
    file_v2: UploadFile = File(...),
):

    name_v1 = file_v1.filename
    name_v2 = file_v2.filename

    content_v1 = await file_v1.read()
    content_v2 = await file_v2.read()

    def parse_files():
        texts = []
        for content in (content_v1, content_v2):
            with pymupdf.open(stream=content, filetype="pdf") as document:
                texts.append("\n".join(page.get_text() for page in document))
        return texts

    text_v1, text_v2 = await run_in_threadpool(parse_files)

    return {
        "summary": str(f"Analyzed {name_v1} and {name_v2} for semantic differences."),
        "changes": [
            {"clause": str("Legal Warrant Clause"), "severity": "high"},
            {"v1_text": text_v1},
            {"v2_text": text_v2},
            {"analysis": "detailed_analysis_text"}
        ]   
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
