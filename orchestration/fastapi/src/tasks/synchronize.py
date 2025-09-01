import logging
from urllib.parse import urljoin

import httpx

from scraper.session_5_scraping import download_file, get_current_submissions
from settings import settings
from worker import worker

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


@worker.task(name="synchronize")
def synchronize(base_url: str) -> None:
    metadata_list = get_current_submissions(base_url=base_url)
    logger.info(f"Found {len(metadata_list)} submissions to synchronize.")
    logger.info(f"{metadata_list[0]}")
    logger.info(f"Starting synchronization with {len(metadata_list)} submissions.")
    for submission in metadata_list:
        payload = {
            "title": submission.title,
            "description": submission.description,
            "author": submission.author,
            "topic": submission.draft_category,
            "href": submission.href,
            "verified": False,
            "session": "5.2",
            "document_type": "insession document",
        }
        id: str | None = None
        try:
            response = httpx.post(
                url=urljoin(
                    str(settings.pocketbase_api.host),
                    "/api/collections/submissions/records",
                ),
                json=payload,
            )
            response.raise_for_status()
            id = response.json().get("id")
        except httpx.RequestError as e:
            raise ValueError(f"Request error while posting submission: {e}") from e
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Request error while posting submission: {e}") from e

    file = download_file(file_url=str(submission.href))
    if not file:
        logger.error(f"Failed to download file from {submission.href}")
        return
    else:
        try:
            files = {
                "file": (
                    str(id) + ".pdf",
                    file,
                    "application/pdf",
                )
            }
            response = httpx.patch(
                url=urljoin(
                    str(settings.pocketbase_api.host),
                    f"/api/collections/submissions/records/{id}",
                ),
                files=files,
            )
            response.raise_for_status()
        except httpx.RequestError as e:
            logger.error(f"Request error while uploading file: {e}")
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error while uploading file: {e}")
    logger.info(f"Submission {submission.title} synchronized successfully.")
