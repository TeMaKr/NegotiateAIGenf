from pathlib import PurePath

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from qdrant_client.models import FieldCondition, Filter, MatchValue
from vector_database.session import inc_vector_store


def parse_file(file_path: str | PurePath) -> Document:
    loader = PyPDFLoader(
        file_path=file_path,
        mode="single",
    )
    document = loader.load()
    return document[0]


def add_metadata(document: Document, doc_id: str, href: str) -> Document:
    document.metadata = {}
    document.metadata.update({"retriever_id": doc_id, "href": href})
    return document


def split_document(document: Document) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=100,  # Reduced to 20% (more efficient, still good context)
        add_start_index=True,
        strip_whitespace=True,
        separators=[
            # Structural separators (try these first)
            "\n\nArticle ",
            "\n\nChapter ",
            "\n\nSection ",
            "\n\n\n",  # Triple line breaks (major sections)
            # Numbered items
            "\n\n",  # Double line breaks (paragraphs)
            r"\n\n(?=\d+\.)",  # Before numbered paragraphs (1. 2. 3.)
            r"\n(?=\([0-9]+\))",  # Before parenthetical numbers (1) (2) (3)
            r"\n(?=\([a-z]\))",  # Before lettered items (a) (b) (c)
            # Your existing fallbacks
            "\n",  # Single line breaks
            ". ",  # Sentence endings
            " ",  # Word boundaries
            "",  # Character level (last resort)
        ],
        is_separator_regex=True,  # Enable regex patterns
    )

    docs_chunked = text_splitter.split_documents(documents=[document])
    return docs_chunked


def enrich_doc_chunks(doc_chunks: list[Document]) -> list[Document]:
    for doc in doc_chunks:
        content = doc.page_content
        updated_content = f"start_index: {doc.metadata.get('start_index', '')} | "
        author = doc.metadata.get("author", None)
        draft_category = doc.metadata.get("draft_category", None)

        if author:
            updated_content += f"author: {author} | "
        if draft_category:
            updated_content += f"article number: {draft_category} | "

        updated_content += f"{content}"
        doc.page_content = updated_content
    return doc_chunks


def upsert_doc_chunks(doc_id: str, doc_chunks: list[Document]) -> None:
    delete_filter = Filter(
        must=[
            FieldCondition(key="metadata.retriever_id", match=MatchValue(value=doc_id))
        ]
    )
    inc_vector_store.client.delete(collection_name="inc", points_selector=delete_filter)
    inc_vector_store.add_documents(doc_chunks)


def process_document(
    file_path: str | PurePath,
    doc_id: str,
    href: str,
) -> list[Document]:
    document = parse_file(file_path=file_path)
    document = add_metadata(document=document, doc_id=doc_id, href=href)
    docs_chunked = split_document(document=document)
    docs_chunked = enrich_doc_chunks(doc_chunks=docs_chunked)
    return docs_chunked


if __name__ == "__main__":
    document = parse_file(
        file_path="https://resolutions.unep.org/incres/uploads/switzerland_suggestions_bra_informal_proposal_on_article_3_0.pdf"
    )
    document = add_metadata(document=document, doc_id="test", href="test")
    docs_chunked = split_document(document=document)
    for doc in docs_chunked:
        print(doc.page_content)
        print("---")
    enriched = enrich_doc_chunks(doc_chunks=docs_chunked)
    for doc in enriched:
        print(doc.page_content)
        print("---")
    pass
