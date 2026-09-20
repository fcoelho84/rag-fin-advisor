from fastapi import APIRouter

from app.services.analyze import analyze as analyzeService

router = APIRouter(prefix="/analyze", tags=["analyze"])


@router.get("/{ticker}")
def analyze(ticker: str):
    response = analyzeService(ticker)

    return response
