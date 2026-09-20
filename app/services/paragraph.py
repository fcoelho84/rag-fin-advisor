import re

import spacy

_natural_language_processor = spacy.load("pt_core_news_sm")


def get_paragraphs(text: str) -> list[str]:
    if not text or not text.strip():
        return []

    text_cleaned = re.sub(r"\s+", " ", text).strip()

    doc = _natural_language_processor(text_cleaned)

    return [sentence.text.strip() for sentence in doc.sents if sentence.text.strip()]
