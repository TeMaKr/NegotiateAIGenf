from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from qdrant_client import QdrantClient
from settings import settings

embeddings = HuggingFaceEmbeddings(
    model_name=settings.vector_store.model,
    model_kwargs={"device": "cpu"},
)


def get_client():
    client = QdrantClient(
        url=settings.vector_store.url,
        api_key=settings.vector_store.api_key,  # not using Secret wrapper here
    )
    return client


def vector_store(client: QdrantClient, collection_name: str) -> QdrantVectorStore:
    return QdrantVectorStore(
        client=client,
        collection_name=collection_name,
        embedding=embeddings,
        retrieval_mode=RetrievalMode.DENSE,
    )


client = get_client()
inc_vector_store = vector_store(client, "inc")
