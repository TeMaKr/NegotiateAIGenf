import json
import logging
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated

from curl_cffi import requests as cffi_requests
from curl_cffi.requests import Response

# Add the src directory to Python path so we can import from models
from models import Metadata
from pydantic import BaseModel, Field, HttpUrl

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

AUTHOR_TAXONOMY = Path(__file__).parent.parent / "taxonomies" / "authors.json"


# with open(AUTHOR_TAXONOMY, "r") as fp:
#     author_taxonomy: list = json.load(fp=fp)

# author_id_mapper = {
#     author["name"]: author["id"] for author in author_taxonomy if "id" in author
# }


def get_random_user_agent():
    """
    Return a random user agent to avoid detection by web servers.
    This function returns a user agent string that mimics a real browser request.
    Returns:
        str: A random user agent string.
    """
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    ]
    return random.choice(user_agents)


def get_enhanced_headers():
    """
    Get enhanced headers that mimic a real browser request to avoid detection.
    Returns:
        dict: A dictionary of headers to be used in the request.
    """
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": (
            "text/html,application/xhtml+xml,application/xml,application/pdf;"
            "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }


def fetch_response(url: str, retries: int = 3) -> Response | None:
    """
    Fetch response using curl-cffi for better TLS fingerprinting evasion and retries.
    Args:
        url (str): The URL to fetch.
        retries (int): The number of retries in case of failure.
    Returns:
        Response | None: The response object if successful, None otherwise.
    """
    for attempt in range(retries):
        try:
            # Add random delay between requests
            if attempt > 0:
                time.sleep(random.uniform(1, 3))

            response = cffi_requests.get(
                url,
                headers=get_enhanced_headers(),
                timeout=30,
                impersonate="chrome136",  # Mimic Chrome 136's TLS fingerprint
                allow_redirects=True,
                verify=True,
            )
            response.raise_for_status()
            return response
        except Exception as e:
            logger.warning(f"httpx attempt {attempt + 1} failed for {url}: {e}")
            if attempt == retries - 1:
                logger.error(f"All httpx attempts failed for {url}")
    return None


def fetch_html(url: str, retries: int = 3) -> str | None:
    """
    Fetches the HTML content from a given URL with retries.
    Args:
        url (str): The URL to fetch the HTML from.
        retries (int): The number of retries in case of failure.
    Returns:
        str | None: The HTML content as a string if successful, None otherwise.
    """
    response = fetch_response(url, retries)
    if response:
        return response.text
    else:
        logger.error(f"Failed to fetch HTML from {url} after {retries} attempts.")
    return None


def parse_a_text(a_text_raw: str) -> str:
    """Parses the raw text from an <a> tag to remove unwanted characters and whitespace.
    Args:
        a_text_raw (str): The raw text from the <a> tag.
    Returns:
        str: The cleaned and parsed text."""
    if not a_text_raw:
        return ""
    parsed_a_text = (
        a_text_raw.replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
        .replace("  ", " ")
    )

    return parsed_a_text


def parse_date(date_str: str) -> datetime:
    """Parses a date string in the format 'dd/mm/yyyy' and returns a datetime object.
    Args:
        date_str (str): The date string to parse.
    Returns:
        datetime: The parsed datetime object."""
    try:
        date = datetime.strptime(date_str, "%d/%m/%Y")
        return date.replace(tzinfo=timezone.utc)
    except ValueError as e:
        if "unconverted data remains" in str(e):
            # Fix 5-digit year like '20223' to '2023' using regex
            date_str = re.sub(r"(\d{2}/\d{2}/)202\d{2}", r"\g<1>2023", date_str)
            try:
                date = datetime.strptime(date_str, "%d/%m/%Y")
                return date.replace(tzinfo=timezone.utc)
            except Exception as e2:
                raise ValueError(f"Error parsing date after correction: {e2}")
        if "does not match format" in str(e):
            # Handle the case where the date format is different
            # For example, 'Monday, January 01, 2023 - 12:00'
            try:
                date = datetime.strptime(date_str, "%d//%m/%Y")
                return date.replace(tzinfo=timezone.utc)
            except Exception as e3:
                raise ValueError(f"Error parsing date after correction: {e3}")
        raise ValueError(f"Error parsing date: {e}")


class UNEPMetadata(BaseModel):
    """Metadata for the UNEP session 5.1 documents."""

    # The following fields are scraped from the contact group html page
    group_of_states: Annotated[
        str | None, Field(title="Group of States", default=None)
    ]  # Multiple states can submit together
    member: Annotated[
        str | None,
        Field(
            title="Member",
        ),
    ]  # Author of the document or spokescountry of the group
    article: Annotated[str | None, Field(title="Article")]  # Category
    description: Annotated[
        str | None, Field(title="Description", default=None)
    ]  # Description of submission if provided
    replacement: Annotated[
        bool, Field(title="Is this a replacement upload?", default=False)
    ]  # Whether the document is a replacement of an earlier submission
    file: Annotated[
        HttpUrl | None, Field(title="File", default=None)
    ]  # URL of the document
    language: Annotated[
        list[str], Field(title="Language", default=[])
    ]  # Languages in which the document is available
    date_of_upload: Annotated[
        datetime | None, Field(title="Date of Upload")
    ]  # Date of submission
    document_type: Annotated[
        str | None, Field(title="Document Type", default=None)
    ]  # Type of document, e.g., "statement"
    # The following fields are automatically set
    # Automatically set the creation time (with microseconds set to zero)
    created_at: Annotated[
        datetime,
        Field(
            default_factory=lambda: datetime.now(timezone.utc).replace(microsecond=0)
        ),
    ]
    updated_at: Annotated[
        datetime | None, Field(default=None)
    ]  # Date of last update (automatically set)


def _post_process_metadata(unep_metadata: UNEPMetadata, session: str) -> Metadata:
    """Post-processes the UNEPMetadata to create a Metadata object.
    Args:
        unep_metadata (UNEPMetadata): The UNEPMetadata object to process.
    Returns:
        Metadata: The processed Metadata object.
    """

    title = (
        str(unep_metadata.file).split("/")[-1].split(".")[0]
        if unep_metadata.file
        else None
    )

    authors = (
        unep_metadata.group_of_states.split(",")
        if unep_metadata.group_of_states
        else unep_metadata.member.split(",")
        if unep_metadata.member
        else []
    )

    # authors_id = [
    #     author_id_mapper[author.strip()]
    #     for author in authors
    #     if author.strip() in author_id_mapper
    # ]

    return Metadata(
        id=None,
        title=title,
        description=unep_metadata.description,
        author=authors,
        draft_category=[unep_metadata.article] if unep_metadata.article else [],
        document_type=unep_metadata.document_type,
        href=str(unep_metadata.file),
        session=session,
    )


def write_metadata_to_file(
    session: str,
    metadata_list: list[UNEPMetadata] | list[Metadata],
):
    # Construct the JSON schema with metadata for the current section
    json_schema = {
        "schema": "https://json-schema.org/draft/2020-12/schema",
        "title": f"UNEP Session {session} Submissions",
        "description": f"Metadata for UNEP session {session} submissions",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "submissions": [metadata.model_dump() for metadata in metadata_list],
    }
    # Serialize the schema and write it to a JSON file
    json_metadata = json.dumps(json_schema, default=str)

    folder_path = Path(__file__).parent.parent / "data" / "raw"
    folder_path.mkdir(parents=True, exist_ok=True)
    output_path = folder_path / f"metadata_session_{session}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(json_metadata)


def download_file(file_url: str) -> bytes | None:
    """Downloads a file from the given URL.
    Args:
        file_url (str): The URL of the file to download.
    Returns:
        bytes | None: The content of the file if successful, None otherwise.
    """
    if not file_url:
        logger.error("No file URL provided.")
        return None
    # Remove query parameters from the URL if they exist
    file_url = file_url.split("?")[0]
    # Remove pound sign and everything after it
    file_url = file_url.split("#")[0]
    if not file_url.endswith(".pdf"):
        logger.error(f"Invalid file URL: {file_url}")
        return None
    pdf_response = fetch_response(file_url, retries=3)
    if pdf_response:
        return pdf_response.content
    logger.error(f"Failed to download file from {file_url} after 3 attempts.")
    return None
