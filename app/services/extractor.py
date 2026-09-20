import base64
import csv
import io
import re
import zipfile
from urllib.parse import urlencode

import httpx
import pymupdf
from bs4 import BeautifulSoup

from app.config import settings


async def _request(
    url: str,
    params: dict[str, str] | None = None,
) -> httpx.Response:
    try:
        async with httpx.AsyncClient(
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/140.0.0.0 Safari/537.36"
                ),
                "Accept": "*/*",
            },
            timeout=90,
            follow_redirects=True,
        ) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()

            return response

    except httpx.HTTPStatusError as e:
        raise RuntimeError(
            f"{e.request.url}: Status Code - {e.response.status_code}"
        ) from e

    except httpx.RequestError as e:
        raise RuntimeError(f"{e.request.url}: {type(e).__name__}: {repr(e)}") from e


async def _extract_cnpj_by_ticker_from_b3(ticker: str) -> str | None:
    response = await _request(
        settings.B3_SEARCH_URL,
        params={"query": ticker.strip().upper()},
    )

    match = re.search(
        r"\b\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}\b",
        response.text,
    )

    return match.group(0) if match else None


async def _get_latest_fre_url_to_download(cnpj: str) -> str | None:

    response = await _request(
        f"{settings.CVM_SEARCH_URL}/CIA_ABERTA/DOC/FRE/DADOS/fre_cia_aberta_2025.zip"
    )

    with zipfile.ZipFile(io.BytesIO(response.content)).open(
        "fre_cia_aberta_2025.csv"
    ) as raw:
        rows = [
            {k.lower(): v for k, v in row.items()}
            for row in csv.DictReader(
                io.TextIOWrapper(raw, encoding="latin-1"),
                delimiter=";",
            )
            if row["CNPJ_CIA"] == cnpj
        ]

    obj = max(
        rows,
        key=lambda r: int(r.get("versao", 0)),
        default=None,
    )

    return f"{settings.CVM_FRE_DOWNLOAD}&{urlencode({'numSequencia': obj['id_doc'], 'numVersao': obj['versao']})}"


async def _get_risk_factor_pdf(url: str) -> str:
    response = await _request(url)

    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        xml_name = next(
            name
            for name in z.namelist()
            if name.lower().endswith(".xml") and "fre" in name.lower()
        )

        with z.open(xml_name) as raw:
            xml_content = raw.read()

    soup = BeautifulSoup(xml_content, "xml")

    riskFactorDesc = soup.find("DescricaoFatoresRisco")

    if not riskFactorDesc:
        raise ValueError("Risk factor section not found.")

    b64PDF = riskFactorDesc.find("ImagemObjetoArquivoPdf")

    if not b64PDF or not b64PDF.text:
        raise ValueError("B64 PDF not found for Risck factor section.")

    pdf_bytes = base64.b64decode("".join(b64PDF.text.split()))

    return pymupdf.open(stream=pdf_bytes, filetype="pdf")


async def extract_risk_factor_text_by_ticker(ticker: str) -> str:
    cnpj = await _extract_cnpj_by_ticker_from_b3(ticker)
    fre = await _get_latest_fre_url_to_download(cnpj)
    document = await _get_risk_factor_pdf(fre)

    try:
        return " ".join(page.get_text() for page in document)
    finally:
        document.close()
