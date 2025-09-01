"""
Preprocess authors in the submissions.

Goal: Replaced author names in the submissions with their identifiers from the taxonomy
      either directly or through additional mappings.

Steps:
1. Use additional mappings to replace authors in the submissions.
    1. Iterate through the submissions and check if href exists in the additional mappings.
    2. If it exists append the the mapped identifier to the authors list.
    3. If the original author is in the list, remove it.
2. Use the taxonomy to replace authors in the submissions.
    1. Iterate through the submissions and check if we can match the author name with the taxonomy:
       comparison:
       - lowercase the author name
       - remove spaces and parentheses
"""

import json
from datetime import datetime, timezone
from pathlib import Path

path = Path(__file__).parent.parent / "data"
RAW_DATA_PATH = path / "raw"
PROCESSED_DATA_PATH = path / "processed"
TAXONOMY_PATH = path / "taxonomies"
MAPPING_FILE = "unmapped_authors_manually.json"


FILES = [
    "metadata_session_1.json",
    "metadata_session_2.json",
    "metadata_session_3.json",
    "metadata_session_4.json",
    "metadata_session_5.json",
]


def import_file(filename: str) -> dict:
    """Import a JSON file from the raw data directory.
    Args:
        filename (str): The name of the JSON file to import.
    Returns:
        dict: The content of the JSON file as a dictionary.
    Raises:
        FileNotFoundError: If the specified file does not exist in the raw data directory.
    """
    # Check if file exists in the output directory
    if (PROCESSED_DATA_PATH / filename).exists():
        input_file_path = PROCESSED_DATA_PATH / filename
    else:
        # If the file does not exist in the processed data directory,
        # use the raw data directory as input
        input_file_path = RAW_DATA_PATH / filename
    with open(input_file_path, "r") as file:
        return json.load(file)


def extract_submissions(content: dict) -> list[dict]:
    """Extract submission information from the content.
    Args:
        filename (str): The name of the JSON file to extract submissions from.
    Returns:
        list[dict]: A list of submissions extracted from the JSON file.
    Raises:
        FileNotFoundError: If the specified file does not exist in the raw data directory.
    """
    return content.get("submissions", [])


def _modify_titles(
    submissions: list[dict[str, str | list]],
) -> list[dict[str, str | list]]:
    """
    Modify the titles of the submissions.
    This function iterates through the list of submissions and modifies the titles
    by cleaning up the title strings, removing extra spaces, underscores, and converting
    them to title case.
    Args:
        submissions (list[dict[str, str | list]]): A list of submissions where each
            submission is a dictionary containing various fields including "title".
    Returns:
        list[dict[str, str | list]]: The updated list of submissions with modified titles.
    """
    for submission in submissions:
        href_splits = submission["href"].split("/")  # type : ignore
        pdf_split = next(filter(lambda x: ".pdf" in x, href_splits), None)
        if pdf_split:
            title = pdf_split.split(".pdf")[0]
        else:
            raise ValueError(f"Title not found in href: {submission['href']}")

        # clean title
        title_cleaned = " ".join(title.split()).replace("_", " ").title().strip()

        submission["title"] = title_cleaned

    return submissions


def _modify_descriptions(
    submissions: list[dict[str, str | list]],
) -> list[dict[str, str | list]]:
    """
    Modify the descriptions of the submissions.
    This function iterates through the list of submissions and modifies the descriptions
    by cleaning up the description strings, removing extra spaces, underscores, and converting
    them to title case.
    Args:
        submissions (list[dict[str, str | list]]): A list of submissions where each
            submission is a dictionary containing various fields including "description".
    Returns:
        list[dict[str, str | list]]: The updated list of submissions with modified descriptions.
    """
    for submission in submissions:
        description = submission.get("description", "")
        if not description or not isinstance(description, str):
            continue

        # Clean up the description by removing extra spaces, underscores, etc
        # and convert to title case
        description = " ".join(description.split()).replace("_", " ").title().strip()

        submission["description"] = description

    return submissions


def preprocess():
    """
    Preprocess the titles in the submissions.
    This function iterates through the predefined list of files,
    imports each file, extracts the submissions, modifies the titles,
    and saves the updated content back to the processed data directory.
    The processed files will have the same names as the original files,
    but will be stored in the processed data directory.
    """
    for filename in FILES:
        # Load the original content from the file
        content = import_file(filename)
        submissions = extract_submissions(content)
        submissions = _modify_titles(submissions)
        submissions = _modify_descriptions(submissions)

        for submission in submissions:
            submission["topic"] = submission.get("draft_category", [])
            submission.pop("draft_category", None)

        content["submissions"] = submissions
        content["timestamp"] = datetime.now(timezone.utc).isoformat()

        with open(PROCESSED_DATA_PATH / filename, "w") as f:
            json.dump(content, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    preprocess()
