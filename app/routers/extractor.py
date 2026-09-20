from fastapi import APIRouter

from app.services.extractor import extract_risk_factor_text_by_ticker

router = APIRouter(prefix="/extractor", tags=["extractor"])


@router.get("/{ticker}")
async def extract_risk_factor(ticker: str) -> str:
    return extract_risk_factor_text_by_ticker(ticker)
