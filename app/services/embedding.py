from sentence_transformers import SentenceTransformer

from app.config import settings

_model = SentenceTransformer(settings.HUGGING_FACE_MODEL)


def generate_embeddings(paragraphs: list[str]) -> list:
    if not paragraphs:
        return []

    return _model.encode(paragraphs).tolist()
