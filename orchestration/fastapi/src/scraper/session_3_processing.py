import logging
import re
from datetime import datetime, timezone

from scraper.generic_scraper import scrape_page
from scraper.helper import UNEPMetadata, parse_a_text, parse_date

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def _parse_surrounding_p(
    text_raw: str, type: str
) -> tuple[str | None, str | None, datetime | None]:
    """Extracts field data from the submission paragraph.
    Args:
        submission (Tag): The submission to extract data from.
    Returns:
        tuple[str, str | None, HttpUrl, datetime]: A tuple containing the author,
            group of states, file URL, and date of upload.
    """

    text = parse_a_text(text_raw)
    if "english" in text.lower():
        text_search = re.search(r"(.*) english", text, re.I)
        if text_search:
            text = text_search.group(1)
    text_parts_raw = text.split("|")
    if len(text_parts_raw) > 1 and "closing" in text_parts_raw[1].lower():
        text_parts_raw = [text_parts_raw[0]]
    text_parts = [t.strip() for t in text_parts_raw]
    date_of_upload = parse_date(text_parts[0]) if len(text_parts) > 1 else None
    members_raw = text_parts[1] if len(text_parts) > 1 else text_parts[0]
    members_raw = (
        re.split(r"\(", string=members_raw)[0]
        if "english" in members_raw.lower()
        else members_raw
    )
    members_list = re.split(
        r"\s*on behalf of the\s*|\s*on behalf of\s*", string=members_raw, flags=re.I
    )
    if len(members_list) > 1:
        members = members_list[0]
        group_of_states = members_list[-1]
    elif (
        len(members_list) == 1
        and (
            len(re.findall(r",", members_list[0])) >= 1
            or len(re.findall(r"\sand\s|,and\s", members_list[0])) >= 1
        )
        and not "bosnia and herzegovina" in members_list[0].lower()
    ):
        members = None
        group_of_states = members_list[0]
    elif len(members_list) == 1 and re.match(
        r"european union|^the group of.*$|^group of.*$|^the allicance of.*$|^alliance of.*$"
        r"|^the group of states of.*$|^group of states of.*$"
        r"|^.*as co-chairs.*$",
        members_list[0],
        flags=re.I,
    ):
        members = None
        group_of_states = members_list[0]

    else:
        members = members_list[0]
        group_of_states = None

    return members, group_of_states, date_of_upload


def parse_data(
    submission: dict, type: str, document_type: str | None, **kwargs
) -> UNEPMetadata:
    """Parses the submission data and returns a UNEPMetadata object."""
    surrounding_p = submission.get("surrounding_p", "")
    author, group_of_states, date_of_upload = _parse_surrounding_p(surrounding_p, type)
    draft_category = kwargs.get("subsection", None)
    if not draft_category:
        draft_category = kwargs.get("section", None)
    a_text = submission.get("a_text", "")
    description = parse_a_text(a_text)
    if not draft_category:
        draft_category = description
    file_url = submission.get("href", None)

    return UNEPMetadata(
        member=author,
        group_of_states=group_of_states,
        article=draft_category if draft_category else "unknown",
        description=description,
        replacement=False,
        file=file_url,
        language=[],
        date_of_upload=date_of_upload,
        created_at=datetime.now(timezone.utc).replace(microsecond=0),
        updated_at=None,
        document_type=document_type,
    )


def scrape(
    base_url: str,
    accordion_names: dict[str, str],
    session: str,
    prevent_duplicate_accordions: bool = True,
    document_type: str | None = None,
) -> list[UNEPMetadata]:
    """Main function to scrape the UNEP session documents."""
    logger.info(f"Starting to scrape session {session}")
    # Scrape the main page and get all submission data
    data = scrape_page(
        base_url, prevent_duplicate_accordions=prevent_duplicate_accordions
    )
    # Iterate over each accordion section and its type
    total_submissions_list = []
    for accordion_name, type in accordion_names.items():
        metadata_list: list[UNEPMetadata] = []
        # Filter submissions that belong to the current accordion section
        for submission in data:
            if submission.get(
                "accordion_name"
            ) != accordion_name and "Part" not in submission.get("accordion_name", ""):
                continue
            # Parse submission data into UNEPMetadata objects
            metadata = parse_data(
                submission,
                type,
                document_type=document_type,
                section=submission.get("section", None),
                subsection=submission.get("subsection", None),
            )
            metadata_list.append(metadata)
        total_submissions_list.extend(metadata_list)
    logger.info(f"Scraping of session {session} completed.")
    return total_submissions_list


if __name__ == "__main__":
    pass
