import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
from bs4 import BeautifulSoup
from bs4.element import Tag
from pydantic import BaseModel, HttpUrl

from models.submissions import Metadata
from scraper.helper import UNEPMetadata, fetch_html

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# This script scrapes the contact groups from the UNEP website for session 5.1
FILE_BASE_URL = "https://resolutions.unep.org"
AUTHOR_TAXONOMY = Path(__file__).parent.parent / "data" / "taxonomies" / "authors.json"
TOPIC_TAXONOMY = Path(__file__).parent.parent / "data" / "taxonomies" / "topics.json"
AUTHOR_ID_MAPPER = (
    Path(__file__).parent.parent
    / "data"
    / "taxonomies"
    / "additional_mappings"
    / "author_id_mapper.json"
)
TOPIC_ID_MAPPER = (
    Path(__file__).parent.parent
    / "data"
    / "taxonomies"
    / "additional_mappings"
    / "topic_id_mapper.json"
)


class ContactGroup(BaseModel):
    """Contact group for the UNEP session 5.1 documents."""

    text: str
    url: HttpUrl


def load_json(path: Path) -> dict[str, Any]:
    """Loads a JSON file from the given path."""
    with open(file=path, encoding="utf-8", mode="r") as file:
        data = json.load(file)
        return data


def parse_contact_groups(html: str) -> list[ContactGroup]:
    """Parses the contact groups from the HTML content.
    Args:
        html (str): The HTML content to parse.
    Returns:
        list[ContactGroup]: A list of ContactGroup objects.
    """
    soup = BeautifulSoup(html, "html.parser")
    content = soup.find("div", id="ContactGroups")
    if not content or not isinstance(content, Tag):
        logger.error("No contact groups found in the response or content is not a Tag.")
        return []

    # Ensure content is a Tag before calling find_all
    contact_groups = [
        cg
        for cg in content.find_all("h4")
        if re.search(r"^.*contactgroup\d{1,2}.*", str(cg.text).replace(" ", "").lower())
    ]

    # Assuming each contact group (cg) has an <a> tag with the URL
    contact_groups_urls = []
    for cg in contact_groups:
        try:
            if not isinstance(cg, Tag):
                raise ValueError("Contact group div is not a valid Tag.")
            a_tag = cg.find("a")  # Find the <a> tag within the contact group
            if (
                a_tag and isinstance(a_tag, Tag) and a_tag.has_attr("href")
            ):  # Check if <a> tag exists and has href
                contact_group_name = cg.text.replace(" >", "").replace(" ", "_").lower()
                contact_group_url = HttpUrl(str(a_tag["href"]))
                contact_groups_urls.append(
                    ContactGroup(text=contact_group_name, url=contact_group_url)
                )
                continue
            raise ValueError("Contact group does not have a valid URL.")
        except ValueError as e:
            logger.error(f"Error processing contact group {cg.text}: {e}")
            continue
    # Return the list of contact groups with URLs
    return contact_groups_urls


def parse_metadata(html: str) -> list[Metadata]:
    """Parses the metadata from the HTML content.

    Args:
        html (str): The HTML content to parse.

    Returns:
        list[UNEPMetadata]: A list of UNEPMetadata objects.
    """
    if not html:
        raise ValueError("HTML content is empty or None")

    soup = BeautifulSoup(html, "html.parser")
    submission_content = soup.find_all("div", id="comments")

    if not submission_content:
        raise ValueError("No submissions found in the response.")

    submission_content = submission_content[0]

    # Ensure submission_content is a Tag before calling find_all
    if not isinstance(submission_content, Tag):
        logger.error("Submission content is not a valid Tag.")
        return []

    submissions = [
        submission
        for submission in submission_content.find_all("div", class_="comment")
    ]
    # Assuming each submission has a <div> with the class "comment"
    if not submissions:
        raise ValueError("No submissions found in the response.")

    # Extract metadata from each submission
    metadata_list = []
    for submission in submissions:
        try:
            if not isinstance(submission, Tag):
                raise ValueError("Submission div is not a valid Tag.")
            # Extract member fields from the submission
            field_mapping = {}
            field_data_fmtd: datetime | str | list[str] | bool | None = None
            for field, info in UNEPMetadata.model_fields.items():
                if field in ["created_at", "updated_at"]:
                    continue
                field_data = _extract_field_data(info.title, submission)  # type: ignore
                if field_data:
                    if field == "date_of_upload":
                        field_data_fmtd = _parse_date(field_data)
                    elif field == "replacement":
                        field_data_fmtd = (
                            True if str(field_data).lower() == "yes" else False
                        )
                    elif field == "language":
                        field_data_fmtd = [str(field_data)]
                    else:
                        field_data_fmtd = str(field_data)
                    field_mapping[field] = field_data_fmtd

            unep_metadata = UNEPMetadata(**field_mapping, updated_at=None)

            metadata_list.append(_post_process_metadata(unep_metadata))
        except ValueError as e:
            logger.error(f"Error processing submission: {e}")
            continue

    return metadata_list


def download_file(file_url: str) -> bytes | None:
    try:
        pdf_response = httpx.get(file_url)
        pdf_response.raise_for_status()
        pdf_bytes = pdf_response.content
    except httpx.HTTPStatusError as e:
        logger.error(f"Failed to download file from {file_url}: {e}")
        return None
    except httpx.RequestError as e:
        logger.error(f"Request error while downloading file from {file_url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while downloading file from {file_url}: {e}")
        return None
    return pdf_bytes


def load_authors_taxonomy() -> set:
    taxonomy = load_json(AUTHOR_TAXONOMY)
    member = taxonomy["member"]

    associations = [taxonomy["name"] for name in taxonomy["country_associations"]]
    authors_processed = [
        author.lower().replace(" ", "").replace("(", "").replace(")", "")
        for author in member + associations
    ]
    return set(authors_processed)


def load_topics_taxonomy() -> set:
    taxonomy = load_json(TOPIC_TAXONOMY)
    categories = [topic["category"] for topic in taxonomy]  # type: ignore
    subcategories = [
        subcategory
        for topic in taxonomy
        for subcategory in topic["subcategory"]  # type: ignore
    ]
    topics_processed = [
        topic.lower().replace(" ", "") for topic in categories + subcategories
    ]
    return set(topics_processed)


def _post_process_metadata(unep_metadata: UNEPMetadata) -> Metadata:
    """Post-processes the UNEPMetadata to create a Metadata object.
    Args:
        unep_metadata (UNEPMetadata): The UNEPMetadata object to process.
    Returns:
        Metadata: The processed Metadata object.
    """

    authors_taxonomy = load_authors_taxonomy()
    authors_id_mapper = load_json(path=AUTHOR_ID_MAPPER)

    topics_taxonomy = load_topics_taxonomy()
    topics_id_mapper = load_json(path=TOPIC_ID_MAPPER)

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

    authors_mapped = []

    for author_collection in authors:
        for author in author_collection:
            authors_collection_mapped = []
            author_processed = (
                author.lower().replace(" ", "").replace("(", "").replace(")", "")
            )
            if author_processed in authors_taxonomy:
                author_id = authors_id_mapper.get(author_processed)
                authors_collection_mapped.append(author_id)
            authors_mapped.append(authors_collection_mapped)

    topic_processed = unep_metadata.topic.lower().replace(" ", "")

    topics_mapped = []

    if topic_processed in topics_taxonomy:
        topic_id = topics_id_mapper.get(topic_processed)
        if topic_id:
            topics_mapped.append(topic_id)

    return Metadata(
        id=None,
        title=title,
        description=unep_metadata.description,
        author=authors_mapped,
        document_type="insession document",
        draft_category=topics_mapped,
        href=str(unep_metadata.file),
        session="5.1",
    )


def _extract_field_data(field_name: str, submission: Tag) -> str | None:
    """Extracts field data from the submission tag.
    Args:
        field_name (str): The name of the field to extract.
        submission (Tag): The submission to extract data from.
    Returns:
        str | None: The extracted field data or None if not found.
    """
    div = submission.find(
        "div",
        attrs={"class": "field-label"},
        string=re.compile(f"^{field_name}.*", re.I),
    )
    if not div:
        logger.debug(f"Field {field_name} not found in the submission.")
        return None
    next_div = div.find_next_sibling("div")
    if not next_div:
        raise ValueError(f"Next div not found for field {field_name}.")

    if not isinstance(next_div, Tag):
        raise ValueError(f"Next div is not a valid Tag for field {field_name}.")

    text = next_div.find_next("div")
    if not isinstance(text, Tag):
        raise ValueError(f"Text div is not a valid Tag for field {field_name}.")

    text = text.string
    if field_name == "File":
        a_tag = next_div.find_next("a")
        if not isinstance(a_tag, Tag):
            raise ValueError(f"File URL not found for {field_name}.")
        if a_tag and a_tag.has_attr("href"):
            file_url_raw = str(a_tag["href"])
            file_url = file_url_raw.replace("/..", FILE_BASE_URL)
            return file_url
        raise ValueError(f"File URL not found for {field_name}.")
    if text:
        return text
    return None


def _parse_date(date_str: str) -> datetime | None:
    """Parses a date string in the format 'Monday, January 01, 2023 - 12:00'
    and returns a datetime object.
    Args:
        date_str (str): The date string to parse.
    Returns:
        datetime: The parsed datetime object."""
    try:
        date = datetime.strptime(date_str, "%A, %B %d, %Y - %H:%M")
        return date.replace(tzinfo=timezone.utc)
    except ValueError as e:
        raise ValueError(f"Error parsing date: {e}")


def get_current_submissions(base_url: str) -> list[Metadata]:
    """Synchronizes the UNEP session 5.1 submissions"""
    html = fetch_html(base_url)
    if not html:
        logger.error("Failed to fetch HTML content.")
        return []
    contact_groups_urls = parse_contact_groups(html)
    metadata_list: list[Metadata] = []

    for contact_group in contact_groups_urls:
        try:
            logger.info(f"Processing contact group: {contact_group.text}")
            cg_html = fetch_html(str(contact_group.url))

            # Check if HTML was successfully fetched before parsing
            if not cg_html:
                logger.error(
                    f"Failed to fetch HTML for contact group: {contact_group.text} - {contact_group.url}"
                )
                continue

            contact_group_metadata_list = parse_metadata(cg_html)
            metadata_list.extend(contact_group_metadata_list)
            logger.info(
                f"Successfully processed {len(contact_group_metadata_list)} submissions from {contact_group.text}"
            )
        except ValueError as e:
            logger.error(f"Error for {contact_group.text}: {e}")
            continue
        except Exception as e:
            logger.error(
                f"Unexpected error processing contact group {contact_group.text}: {e}"
            )
            continue

    logger.info(f"Total metadata collected: {len(metadata_list)}")
    return metadata_list
