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
    input_file_path = RAW_DATA_PATH / filename
    with open(input_file_path, "r") as file:
        return json.load(file)


def _import_all_author_taxonomy() -> set[str]:
    """
    Import the author taxonomy from the taxonomy directory.
    This function reads a JSON file that contains the author taxonomy and returns a set of
    author names. The taxonomy includes country associations and individual authors.
    Returns:
        set[str]: A set of author names from the taxonomy.
    """
    with open(TAXONOMY_PATH / "authors.json", "r") as file:
        content = json.load(file)

    tax_authors_groups = {
        str(author_group.get("name"))
        for author_group in content.get("country_associations", [])
        if isinstance(author_group, dict)
    }
    tax_authors_members = {str(author) for author in content.get("members", [])}

    tax_authors: set[str] = set(tax_authors_groups).union(tax_authors_members)

    return tax_authors


def _import_group_author_taxonomy() -> list[tuple[str, list[str]]]:
    """
    Import the author taxonomy from the taxonomy directory.
    This function reads a JSON file that contains the author taxonomy and returns a set of
    author names. The taxonomy includes country associations and individual authors.
    Returns:
        set[tuple[str, list[str]]]: A set of tuples containing group names and their members.
    """
    with open(TAXONOMY_PATH / "authors.json", "r") as file:
        content = json.load(file)

    # Extract country associations as tuples of (name, members)
    tax_authors_groups = [
        (str(author_group.get("name")), author_group.get("members", []))
        for author_group in content.get("country_associations", [])
        if isinstance(author_group, dict)
    ]

    return tax_authors_groups


def _import_additional_mappings() -> dict:
    """Import additional mappings from the taxonomy directory.
    This function reads a JSON file that contains mappings of authors to their identifiers
    and the associated hrefs. It returns a dictionary where each key is an href and the
    value is a list of tuples containing the author name and its mapped identifier.
    Returns:
        dict: A dictionary mapping hrefs to a list of tuples (author, mapped_author).
    """
    with open(TAXONOMY_PATH / "additional_mappings" / MAPPING_FILE, "r") as file:
        content = json.load(file)
    mapping_dict = dict[str, list[tuple[str, str] | None]]()
    for author, details in content.items():
        hrefs = details["hrefs"]
        mapped_author = details["mapping"]
        for href, is_valid in hrefs.items():
            # Skip if the href is not valid
            if not is_valid:
                continue
            if href not in mapping_dict:
                mapping_dict[href] = []
            # Append the author and mapped author to the list for this href
            # author is the original author name, mapped_author is the identifier
            # original author name is not used in the mapping, only for debugging purposes
            mapping_dict[href].append((author, mapped_author))

    return mapping_dict


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


def _replace_authors_by_mapping(
    submissions: list[dict[str, str | list]],
) -> list[dict[str, str | list]]:
    """
    Replace names in submissions["authors"] list with their identifiers from the additional mappings.
    This function checks if the href of a submission exists in the additional mappings.
    If it does, it replaces the author names with their mapped identifiers.
    Args:
        submissions (list[dict[str, str | list]]): A list of submissions where each
            submission is a dictionary
            containing an "href" key and an "authors" key.
    Returns:
        list[dict[str, str | list]]: The updated list of submissions
            with authors replaced by their identifiers
            from the additional mappings.
    Raises:
        KeyError: If a submission does not contain the "href" or "authors" key.
    Notes:
        - The "authors" key can be a string or a list of strings.
        - If the "authors" key is a string, it is converted to a list for consistency.
        - If a mapped author is already in the authors list, it is not added again.
        - If the original author is in the authors list, it is removed after adding the mapped author.
    """
    additional_mappings = _import_additional_mappings()

    for submission in submissions:
        authors = submission.get("author", [])
        if not isinstance(authors, list):
            authors = [authors]
        href = submission.get("href", "")

        if href in additional_mappings:
            # If href exists in additional mappings, replace authors completely
            authors = []
            for _, mapped_author in additional_mappings[href]:
                if mapped_author not in authors:
                    authors.append(mapped_author) if isinstance(
                        mapped_author, str
                    ) else authors.extend(mapped_author)
        # deduplicate authors
        authors = list(set(authors))
        submission["author"] = authors

    return submissions


def _replace_authors_by_taxonomy(
    submissions: list[dict[str, str | list]],
) -> list[dict[str, str | list]]:
    """
    Replace names in submissions["authors"] list with their identifiers from the taxonomy.
    This function checks if the author names can be matched with the taxonomy.
    It normalizes the author names by converting them to lowercase, removing spaces and parentheses,
    and then checks if they exist in the set of authors from the taxonomy.
    Args:
        submissions (list[dict[str, str | list]]): A list of submissions where each
            submission is a dictionary containing an "authors" key.
    Returns:
        list[dict[str, str | list]]: The updated list of submissions with
            authors replaced by their identifiers
            from the taxonomy.
    Raises:
        KeyError: If a submission does not contain the "authors" key.
    Notes:
        - The "authors" key can be a string or a list of strings.
        - If the "authors" key is a string, it is converted to a list for consistency.
        - The author names are normalized by converting them to lowercase,
          removing spaces, and parentheses before checking against the taxonomy.
    """

    tax_authors = _import_all_author_taxonomy()
    normalized_tax_authors = {
        author.lower().replace(" ", "").replace("(", "").replace(")", ""): author
        for author in tax_authors
    }

    for submission in submissions:
        authors = submission.get("author", [])
        if not isinstance(authors, list):
            authors = [authors]

        # Replace author names with identifiers from the taxonomy
        for i, author in enumerate(authors):
            normalized_author = (
                author.lower().replace(" ", "").replace("(", "").replace(")", "")
            )
            if normalized_author in normalized_tax_authors.keys():
                authors[i] = normalized_tax_authors[normalized_author]

        submission["author"] = authors

    tax_groups = _import_group_author_taxonomy()

    # Replace group author names with all members of group from the taxonomy
    for submission in submissions:
        authors = submission.get("author", [])
        if isinstance(authors, str):
            authors = [authors]

        # Create a new list to avoid modifying the list we're iterating over
        new_authors = []
        for author in authors:
            # Check if this author is a group name
            is_group = False
            for group_name, members in tax_groups:
                if author == group_name:
                    # Add all members of the group instead of the group name
                    new_authors.extend(members)
                    new_authors.append(group_name)  # Keep the group name for reference
                    is_group = True
                    break

            # If not a group, keep the original author
            if not is_group:
                new_authors.append(author)

        # Remove duplicates and update the submission
        submission["author"] = list(set(new_authors))

    return submissions


def replace_authors(
    submissions: list[dict[str, str | list]],
) -> list[dict[str, str | list]]:
    """
    Replace author names in the submissions with their identifiers from the taxonomy.
    This function first replaces authors using additional mappings and then uses the taxonomy
    to ensure all authors are correctly identified.
    """
    submissions = _replace_authors_by_mapping(submissions)
    submissions = _replace_authors_by_taxonomy(submissions)
    return submissions


def preprocess() -> None:
    """
    Preprocess authors in the submissions of a given file.
    This function imports the file, extracts submissions, replaces authors,
    and returns the updated submissions.
    Args:
        filename (str): The name of the JSON file to preprocess.
    Returns:
        list[dict[str, str | list]]: The updated list of submissions with authors replaced.
    """
    for filename in FILES:
        # Check if file exists in the output directory

        file = import_file(filename)
        submissions = extract_submissions(file)
        submissions = replace_authors(submissions)
        file["submissions"] = submissions
        file["timestamp"] = datetime.now(timezone.utc).isoformat()

        with open(PROCESSED_DATA_PATH / filename, "w") as f:
            json.dump(file, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    preprocess()
