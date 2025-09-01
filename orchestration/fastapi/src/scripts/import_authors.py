import json
import logging
from pathlib import Path
from typing import Any

import httpx
from settings import settings

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

AUTHORS = Path(__file__).parent.parent / "data" / "taxonomies" / "authors.json"

AUTHOR_ID_MAPPER = (
    Path(__file__).parent.parent
    / "data"
    / "taxonomies"
    / "additional_mappings"
    / "author_id_mapper.json"
)


def load_json(path: Path) -> dict[str, Any]:
    with open(file=path) as file:
        data = json.load(file)
    return data


def process_taxonomy(
    raw_data: dict[str, list[str] | dict[str, str | list[str]]],
    author_id_mapper: dict[str, str],
) -> list[dict[str, str]]:
    """Process the taxonomy data to generate a list of author records for database"""
    authors: list[dict[str, str]] = []

    members: list["str"] = raw_data["members"]  # type: ignore

    associations: list["str"] = [
        association["name"]  # type: ignore
        for association in raw_data["country_associations"]
    ]

    for member in members:
        member_id = author_id_mapper[member]
        authors.append({"id": member_id, "name": member, "type": "country"})

    for association in associations:
        association_id = author_id_mapper[association]
        authors.append(
            {"id": association_id, "name": association, "type": "association"}
        )
    return authors


def import_authors() -> None:
    raw_data = load_json(path=AUTHORS)  # type: ignore
    author_id_mapper = load_json(path=AUTHOR_ID_MAPPER)  # type: ignore

    authors = process_taxonomy(raw_data=raw_data, author_id_mapper=author_id_mapper)

    url = f"{settings.pocketbase_api.host}/api/collections/authors/records"

    for author in authors:
        try:
            response = httpx.post(
                url=url,
                json=author,
                headers={"X-API-TOKEN": settings.pocketbase_api.token},
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            continue
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e}")
            continue
