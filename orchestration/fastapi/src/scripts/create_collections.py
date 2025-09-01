"""This script creates the necessary collections. It's intended to be run once to set up
the vector store."""

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
from qdrant_client.models import PayloadSchemaType
from settings import settings


def get_client():
    client = QdrantClient(
        url=settings.vector_store.url,
        api_key=settings.vector_store.api_key,  # not using Secret wrapper here
    )
    return client


def create_collection(client, collection_name: str) -> None:
    if client.collection_exists(collection_name):
        return None
    client.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=settings.vector_store.embedding_dim,
            distance=Distance(settings.vector_store.similarity),
        ),
    )


def create_payload_index(
    client, collection_name: str, field_name, field_schema: PayloadSchemaType
) -> None:
    client.create_payload_index(
        collection_name=collection_name,
        field_name=field_name,
        field_schema=field_schema,
    )


def create_collections():
    client = get_client()
    inc_collection_name = "inc"
    create_collection(client=client, collection_name=inc_collection_name)
    create_payload_index(
        client=client,
        collection_name=inc_collection_name,
        field_name="metadata.retriever_id",
        field_schema=PayloadSchemaType.KEYWORD,
    )
