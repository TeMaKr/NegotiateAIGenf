import logging
import os
from typing import Any

import httpx
from qdrant_client.http.models import FieldCondition, Filter, MatchValue

from settings import settings
from tools import llm_provider
from tools.analyse_submissions import extract_relevant_sentences
from worker import worker

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@worker.task(name="augmentation")
def augment(
    submission_id: str,
    retriever_id: str,
    key_elements: list[str],
    article: str,
) -> None:
    os.environ["OPENAI_API_KEY"] = settings.llm_provider.api_key
    llm = llm_provider.get_llm()

    payload: dict[str, Any] = {"key_element": {key: "" for key in key_elements}}
    filter = Filter(
        must=[
            FieldCondition(
                key="metadata.retriever_id", match=MatchValue(value=retriever_id)
            )
        ]
    )
    # logger.info(key_elements, article)

    for search_key_element in key_elements:
        try:
            result = extract_relevant_sentences(
                search_key_element=search_key_element,
                article=article,
                key_elements=key_elements,
                llm=llm,
                filter=filter,
            )
            if result:
                payload["key_element"][search_key_element] = result
        except Exception as e:
            logger.error(f"Error processing key element {search_key_element}: {e}")
            del payload["key_element"]
            payload["verified"] = False
            break

    try:
        response = httpx.patch(
            f"{settings.pocketbase_api.host}/api/collections/submissions/records/{submission_id}",  # noqa: E501
            json=payload,
            headers={"X-API-TOKEN": settings.pocketbase_api.token},
        )
        response.raise_for_status()
    except httpx.RequestError as e:
        logger.error(f"Request error while updating submission {submission_id}: {e}")
        return
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error while updating submission {submission_id}: {e}")
        return
    logger.info(
        f"Successfully updated submission {submission_id} with key elements: {key_elements}"  # noqa: E501
    )
