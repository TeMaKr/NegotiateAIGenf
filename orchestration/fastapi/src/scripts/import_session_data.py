import io
import json
import logging
import tarfile
from pathlib import Path
from typing import Any

import httpx

from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOPIC_ID_MAPPER = (
    Path(__file__).parent.parent
    / "data"
    / "taxonomies"
    / "additional_mappings"
    / "topic_id_mapper.json"
)

AUTHOR_ID_MAPPER = (
    Path(__file__).parent.parent
    / "data"
    / "taxonomies"
    / "additional_mappings"
    / "author_id_mapper.json"
)


def load_json(path: Path) -> dict[str, Any]:
    with open(file=path, encoding="utf-8", mode="r") as file:
        data = json.load(file)
        return data


def _clean_pdf_file_path(path: str) -> str:
    return path.split("/")[-1].replace("._", "")


def load_pdf_files(path: Path) -> dict[str, bytes]:
    pdf_files = {}

    with tarfile.open(path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile() and member.name.lower().endswith(".pdf"):
                cleaned_name = _clean_pdf_file_path(member.name)
                extracted_file = tar.extractfile(member)
                if extracted_file:
                    # Read the content as bytes to avoid closed file issues
                    pdf_files[cleaned_name] = extracted_file.read()
    return pdf_files


def process_records(
    records: list[dict[str, Any]],
    pdf_files: dict[str, bytes],
    ids_author_mapping: dict[str, str],
    ids_topic_mapping: dict[str, str],
) -> None:
    processed_records = []
    record_files = []

    for record in records:
        authors_id = []
        for author in record["author"]:
            if author in ids_author_mapping:
                authors_id.append(ids_author_mapping[author])

        topics_id = []
        for topic in record["topic"]:
            if topic in ids_topic_mapping:
                topics_id.append(ids_topic_mapping[topic])

        processed_record = {
            "id": record["id"],
            "title": record["title"],
            "description": record["description"],
            "author": authors_id,
            "topic": topics_id,
            "href": record["href"],
            "verified": record["verified"],
            "session": record["session"],
            "document_type": record["document_type"],
        }
        processed_records.append(processed_record)

        file_url = record["href"].split(".pdf")[0]
        file_name = f"{file_url.split('/')[-1]}.pdf".replace("._", "")
        if file_name in pdf_files:
            # Create file-like object from bytes for upload
            pdf_content = pdf_files[file_name]
            file_obj = {
                "file": (
                    file_name,
                    io.BytesIO(pdf_content),
                    "application/pdf",
                )
            }
            record_files.append(file_obj)
        else:
            raise FileNotFoundError(
                f"PDF file '{file_name}' not found in provided files."
            )

    url = f"{settings.pocketbase_api.host}/api/collections/submissions/records"

    for idx, submission in enumerate(processed_records):
        submission_response = None
        try:
            submission_response = httpx.post(
                url=url,
                json=submission,
                headers={"X-API-TOKEN": settings.pocketbase_api.token},
            )
            submission_response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            continue  # Skip file upload if submission failed
        except httpx.HTTPStatusError as e:
            logger.error(f"Request error: {e}")
            continue  # Skip file upload if submission failed

        # Only proceed with file upload if submission was successful
        if submission_response:
            try:
                file_response = httpx.patch(
                    url=f"{settings.pocketbase_api.host}/api/collections/submissions/records/{submission_response.json().get('id')}",  # noqa: E501
                    files=record_files[idx],
                    headers={"X-API-TOKEN": settings.pocketbase_api.token},
                )
                file_response.raise_for_status()
                if (
                    settings.environment.environment in ["LOCAL"]
                    and submission["session"] == "5.1"
                ):
                    if idx < 5:
                        # Update verified status
                        verify_response = httpx.patch(
                            url=f"{settings.pocketbase_api.host}/api/collections/submissions/records/{submission_response.json().get('id')}",  # noqa: E501
                            json={"verified": True},
                            headers={"X-API-TOKEN": settings.pocketbase_api.token},
                        )
                        verify_response.raise_for_status()
                    else:
                        continue
                else:
                    verify_response = httpx.patch(
                        url=f"{settings.pocketbase_api.host}/api/collections/submissions/records/{submission_response.json().get('id')}",  # noqa: E501
                        json={"verified": True},
                        headers={"X-API-TOKEN": settings.pocketbase_api.token},
                    )
                verify_response.raise_for_status()
            except FileNotFoundError as e:
                logger.error(f"Request error: {e}")
                continue
            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                continue
            except httpx.HTTPStatusError as e:
                logger.error(f"Request error: {e}")
                continue


def import_session_data() -> None:
    sessions = [1, 2, 3, 4, 5]

    author_id_mapper = load_json(path=AUTHOR_ID_MAPPER)
    topic_id_mapper = load_json(path=TOPIC_ID_MAPPER)

    for session in sessions:
        metadata_path = (
            Path(__file__).parent.parent
            / "data"
            / "processed"
            / f"metadata_session_{session}.json"
        )
        file_path = (
            Path(__file__).parent.parent
            / "data"
            / "pdf_files"
            / f"metadata_session_{session}.tar.gz"
        )

        session_data = load_json(path=metadata_path)["submissions"]
        pdf_files = load_pdf_files(path=file_path)

        process_records(
            records=session_data,
            pdf_files=pdf_files,
            ids_author_mapping=author_id_mapper,
            ids_topic_mapping=topic_id_mapper,
        )
