from qdrant_client import QdrantClient

from app.config import settings

_client = QdrantClient(
    url=settings.QDRANT_CLUSTER_URL,
    api_key=settings.QDRANT_API_KEY,
    cloud_inference=True,
)


def upsert(points: list):
    _client.upsert(collection_name="my-collection", points=points)
