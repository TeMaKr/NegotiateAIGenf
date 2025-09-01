import logging

import httpx

from settings import settings
from tasks import augment
from vector_database.collections import inc
from worker import worker

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@worker.task(name="embed")
def embed(
    file_path: str,
    submission_id: str,
    retriever_id: str,
    href: str,
    session: str,
    key_elements: dict[str, list[str]] | None = None,
) -> None:
    try:
        doc_chunks = inc.process_document(
            file_path=file_path, doc_id=retriever_id, href=href
        )
        inc.upsert_doc_chunks(doc_id=retriever_id, doc_chunks=doc_chunks)
        logger.info(f"Document {file_path} processed and upsert successfully.")
    except Exception as e:
        logger.error(f"Error processing document {file_path}: {e}")
        payload = {"verified": False}
        try:
            response = httpx.patch(
                f"{settings.pocketbase_api.host}/api/collections/submissions/records/{submission_id}",  # noqa: E501
                json=payload,
                headers={"X-API-TOKEN": settings.pocketbase_api.token},
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(
                f"Request error while updating submission {submission_id}: {e}"
            )
            return

    if session in ["1", "2", "3", "4"]:
        logger.info(
            f"Submission {submission_id} is in session {session}. Augmentation will be skipped."  # noqa: E501
        )
        return

    logger.warning("Key elements for submission %s: %s", submission_id, key_elements)

    if key_elements is None:
        logger.warning(
            f"No key elements provided for submission {submission_id}. Skipping augmentation."
        )
        return
    else:
        for article, elements in key_elements.items():
            logger.warning("Augmentation will be performed for article: %s", article)
            augment.delay(
                submission_id=submission_id,
                retriever_id=retriever_id,
                key_elements=elements,
                article=article,
            )
        return
