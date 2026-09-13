import os

from fastapi import FastAPI, Header, HTTPException

from app.pipeline import run_pipeline
from app.database import get_companies


app = FastAPI(
    title="LH2 Company Intelligence API",
    description="Company intelligence automation agent",
    version="1.0.0",
)


API_SECRET = os.getenv("API_SECRET")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "LH2 Company Intelligence API",
    }


@app.get("/companies")
def companies():
    results = get_companies()

    return {
        "count": len(results),
        "companies": results,
    }


@app.post("/pipeline/run")
def pipeline_run(
    x_api_key: str | None = Header(default=None)
):
    if not API_SECRET:
        raise HTTPException(
            status_code=500,
            detail="API_SECRET is not configured",
        )

    if x_api_key != API_SECRET:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
        )

    run_pipeline()

    return {
        "status": "completed",
        "message": "Pipeline execution completed",
    }