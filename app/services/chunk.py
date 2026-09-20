from typing import Iterator

from transformers import AutoTokenizer

from app.config import settings

_tokenizer = AutoTokenizer.from_pretrained(settings.HUGGING_FACE_MODEL)


def create_chunks(paragraphs: list[str], max_tokens: int = 256) -> list[str]:
    chunks = []
    current_tokens = []

    for para in paragraphs:
        para_tokens = _tokenizer.encode(para, truncation=False)

        for token in para_tokens:
            current_tokens.append(token)

            if len(current_tokens) == max_tokens:
                chunk_text = _tokenizer.decode(current_tokens, skip_special_tokens=True)
                chunks.append(chunk_text)
                current_tokens = []

    if current_tokens:
        chunk_text = _tokenizer.decode(current_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)

    return chunks
