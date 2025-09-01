import json
import logging
from pathlib import Path

import httpx
from settings import settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

TOPIC_TAXONOMY = Path(__file__).parent.parent / "data" / "taxonomies" / "topics.json"
KEY_ELEMENTS = (
    Path(__file__).parent.parent / "data" / "taxonomies" / "key_elements.json"
)
TOPIC_ID_MAPPER = (
    Path(__file__).parent.parent
    / "data"
    / "taxonomies"
    / "additional_mappings"
    / "topic_id_mapper.json"
)


def load_json(path: Path) -> list[dict] | dict[str, list[str] | str]:
    with open(file=path) as file:
        data = json.load(file)
    return data


def process_taxonomy(
    raw_data: list[dict],
    key_elements: dict[str, list[str]],
    topic_id_mapper: dict[str, str],
) -> list[dict[str, str | list[str]]]:
    """Process the taxonomy data to generate a list of author records for database"""
    topics: list[dict[str, str | list[str]]] = []
    topic_names: list[str] = []
    ids_subcategory_mapping: dict[str, str] = {}

    list_of_all_categories = set([topic["category"] for topic in raw_data])

    for topic in raw_data:
        topic_subcategories = topic.get("subcategories", [])
        for subcategory in topic_subcategories:
            if subcategory in list_of_all_categories:
                continue
            if subcategory in topic_names:
                existing_index = next(
                    i for i, t in enumerate(topics) if t["name"] == subcategory
                )
                existing_record = topics[existing_index]
                new_key_elements = key_elements.get(str(topic["article"]), [])
                new_article = str(topic["article"])

                # Update the existing record in place
                existing_key_elements = existing_record["key_element"]
                if isinstance(existing_key_elements, list):
                    topics[existing_index]["key_element"] = (
                        existing_key_elements + new_key_elements
                    )
                existing_article = existing_record["article"]
                if isinstance(existing_article, str):
                    topics[existing_index]["article"] = (
                        f"{existing_article};{new_article}"
                    )
            else:
                topic_id = topic_id_mapper[subcategory]
                ids_subcategory_mapping[subcategory] = topic_id

                record: dict[str, str | list[str]] = {
                    "id": topic_id,
                    "name": subcategory,
                    "key_element": key_elements.get(topic["article"], []),  # type: ignore
                    "article": topic["article"],
                }
                topics.append(record)
                topic_names.append(str(record["name"]))

        parent_topic_id = topic_id_mapper[topic["category"]]

        relevant_subcategory_ids = []

        for subcategory in topic_subcategories:
            if subcategory in ids_subcategory_mapping:
                relevant_subcategory_ids.append(ids_subcategory_mapping[subcategory])

        record: dict[str, str | list[str]] = {
            "id": parent_topic_id,
            "name": topic["category"],
            "key_element": key_elements.get(topic["article"], []),  # type: ignore
            "article": topic["article"],
            "child": relevant_subcategory_ids,
        }
        topics.append(record)
        topic_names.append(str(record["name"]))

    return topics


def import_topics() -> None:
    topics: list[dict] = load_json(path=TOPIC_TAXONOMY)  # type: ignore

    key_elements: dict[str, list[str]] = load_json(path=KEY_ELEMENTS)  # type: ignore

    topic_id_mapper: dict[str, str] = load_json(path=TOPIC_ID_MAPPER)  # type: ignore

    topics = process_taxonomy(
        raw_data=topics, key_elements=key_elements, topic_id_mapper=topic_id_mapper
    )

    url = f"{settings.pocketbase_api.host}/api/collections/topics/records"

    for topic in topics:
        try:
            response = httpx.post(
                url=url,
                json=topic,
                headers={"X-API-TOKEN": settings.pocketbase_api.token},
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            continue
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            continue
