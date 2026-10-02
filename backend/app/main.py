from fastapi import FastAPI


Run: uvicorn app.main:app --reload

Run: uvicorn main:app --host 0.0.0.0 --port 8000


app = FastAPI(title="legal-ai-parser")


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/analyze")
async def analyze(
    file_v1: UploadFile = File(...),
    file_v2: UploadFile = File(...),
):

    name_v1 = file_v1.filename
    name_v2 = file_v2.filename

    # TODO: parse the files

    return {
        "summary": "Compared v1 and v2 successfully.",
        "changes": [
            {"clause": "Legal warranties", "change": "Added new clause regarding warranties."},
            "severity": "minor",
            "v1_text": "Landlord warrants that the property is free from any encumbrances.",
            "v2_text": "Landlord warrants that the property is not free from any encumbrances and defects."
            "analysis": "The change in the legal warranties clause is minor, as it clarifies the landlord's obligations regarding encumbrances and defects. However, it does not significantly alter the overall meaning of the clause."
            
        ]   
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)