"""
Preprocess draft categories in the submissions.

Goal: Replaced draft categories in the submissions with their identifiers from the taxonomy
      either directly or through additional mappings.

Steps:
1. Use the mapping for session 3-4 to replace the draft categories in the submissions.
    1. Iterate through the submissions and check if the draft category exists in the mappings.
    2. If it exists append the the mapped identifiers to the draft categories
       and remove the original draft category.
2. Use the mapping for session 5 to replace the draft categories in the submissions.
    1. Iterate through the submissions and check if the draft category exists in the mappings.
    2. If it exists append the the mapped identifiers to the draft categories
       and remove the original draft category.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from settings import settings

path = Path(__file__).parent.parent / "data"
RAW_DATA_PATH = path / "raw"
PROCESSED_DATA_PATH = path / "processed"
TAXONOMY_PATH = path / "taxonomies"
MAPPING_5_FILE = "draft_category_mapper_session_5_manually.json"

FILES = [
    "metadata_session_3.json",
    "metadata_session_3_manually_finished.json",
    "metadata_session_4.json",
    "metadata_session_4_manually_finished.json",
    "metadata_session_5.json",
    "metadata_session_5_manually_finished.json",
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


def _extract_submissions(content: dict) -> list[dict]:
    """Extract submission information from the content.
    Args:
        filename (str): The name of the JSON file to extract submissions from.
    Returns:
        list[dict]: A list of submissions extracted from the JSON file.
    Raises:
        FileNotFoundError: If the specified file does not exist in the raw data directory.
    """
    return content.get("submissions", [])


def _load_data(identifier: list[str]) -> list[dict[str, str | list]]:
    """
    Load the data from the raw data directory.
    Args:
        identifier (list[str]): A list of identifier strings to filter the files.
    Returns:
        list[dict[str, str | list]]: A list of submissions extracted from the JSON files.
    Raises:
        FileNotFoundError: If the specified file does not exist in the raw data directory.
    """
    submissions = []
    # Check if any identifier string is present in the file name
    files = [file for file in FILES if any(id_str in file for id_str in identifier)]
    for file in files:
        content = import_file(file)
        submissions.extend(_extract_submissions(content))
    return submissions


def match_submissions(
    session: str | None = None,
) -> list[dict[str, str | list]]:
    """
    Match submissions from session 3 or 4 with their manually curated draft categories.
    This function creates a mapping dictionary that maps the original draft categories
    to the manually curated ones.
    Args:
        session (str | None): The session number to process. Defaults to None.
    Returns:
        list[dict[str, str | list]]: A list of processed submissions with updated draft categories.
    Raises:
        ValueError: If the session number is not supported (not "3" or "4").
        FileNotFoundError: If the mapping file does not exist.
    """

    if session not in ["3", "4", "5"]:
        raise ValueError(f"Session {session} is not supported.")

    def _load_mapping_5() -> dict[str, str]:
        """
        Load the mappings from the session 5 topic mappings file.
        """
        # Load the mappings from the mapping files
        mapping_path = TAXONOMY_PATH / "additional_mappings" / MAPPING_5_FILE
        if not mapping_path.exists():
            raise FileNotFoundError(
                f"Mapping file {mapping_path} does not exist. Please add the file first."
            )

        with open(mapping_path, "r", encoding="utf-8") as file:
            mapping_dict = json.load(file)

        return mapping_dict

    def _normalize(str) -> str:
        """
        Normalize a string by converting it to lowercase and removing spaces and parentheses.
        """
        return str.lower().replace(" ", "").replace("(", "").replace(")", "")

    def _to_list(value: str | list) -> list[str]:
        """
        Ensure the value is a list, converting it if necessary.
        """
        if isinstance(value, str):
            return [value]
        elif isinstance(value, list):
            return value
        else:
            raise ValueError(f"Expected a string or list, got {type(value)}")

    mapping_dict: dict[str, dict[str, list]] = {}
    original_data = _load_data([f"{session}.json"])
    manually_curated_data = _load_data([f"{session}_manually_finished.json"])

    # Iterate through the manually curated data and create the mapping dictionary
    processed_submissions = []
    for submission in original_data:
        href = submission.get("href", None)
        if not href or not isinstance(href, str):
            continue
        topics = submission.get("draft_category", [])
        if isinstance(topics, str):
            topics = [topics]

        if href not in mapping_dict:
            mapping_dict[href] = {}
        # Find the corresponding manually curated submission
        for curated_submission in manually_curated_data:
            if curated_submission.get("href") == href:
                mapped_topics = curated_submission.get("draft_category", [])
                if isinstance(mapped_topics, str):
                    mapped_topics = [mapped_topics]
                mapping_dict[href]["original"] = topics
                mapping_dict[href]["mapped"] = mapped_topics
                submission["draft_category"] = mapped_topics
                processed_submissions.append(submission)

    # If session is 5, load the mapping from the session 5 topic mappings file
    if session == "5":
        mapping_dict_5 = _load_mapping_5()
        normalized_mappings = {
            _normalize(original): _to_list(replacement)
            for original, replacement in mapping_dict_5.items()
        }

        # Update the processed submissions with the mapped topics
        for submission in processed_submissions:
            topics = submission.get("draft_category", [])
            if isinstance(topics, str):
                topics = [topics]

            # Replace topics with their identifiers from the mapping
            processed_topics = []
            for topic in topics:
                normalized_topic = _normalize(topic)
                if normalized_topic in normalized_mappings.keys():
                    processed_topics.extend(normalized_mappings[normalized_topic])
            if processed_topics:
                submission["draft_category"] = processed_topics
    # For Debugging purposes only
    if settings.environment.environment == "LOCAL":
        # Save the mapping dictionary to a JSON file
        mapping_file_path = (
            TAXONOMY_PATH
            / "additional_mappings"
            / f"draft_category_mapper_session_{session}_automated_finished.json"
        )
        # Ensure the directory exists
        mapping_file_path.parent.mkdir(parents=True, exist_ok=True)
        # Write the mapping dictionary to the file
        with open(mapping_file_path, "w", encoding="utf-8") as file:
            json.dump(mapping_dict, file, indent=2, ensure_ascii=False)

    return processed_submissions


def preprocess() -> None:
    """
    Preprocess the draft categories in the submissions.
    This function processes the submissions from session 3, 4, and 5,
    replacing the draft categories with their identifiers from the taxonomy.
    Args:
        input_file_path (Path): The path to the directory containing the input files.
            Defaults to PROCESSED_DATA_PATH as it is assumed that the files are already processed
            by a previous step and are ready for further processing.
    Returns:
        None: The function modifies the files in place, saving the updated submissions
              back to the processed data directory.
    Raises:
        ValueError: If the session number is not recognized in the file names.
        FileNotFoundError: If the input file does not exist in the specified directory.
    """
    original_data = [file for file in FILES if "manually" not in file]
    for file in original_data:
        if "3" in file:
            session = "3"
        elif "4" in file:
            session = "4"
        elif "5" in file:
            session = "5"
        else:
            raise ValueError(f"Unknown session in file name: {file}")

        submissions = match_submissions(session)

        # Sort submissions alphabetically by title
        sorted_submissions = sorted(
            submissions,
            key=lambda x: x.get("title", ""),
        )
        # sort topics in each submission alphabetically
        for submission in sorted_submissions:
            if "draft_category" in submission:
                submission["draft_category"] = sorted(submission["draft_category"])

        content = import_file(file)

        # Update the content with the modified submissions
        content["submissions"] = submissions
        content["timestamp"] = datetime.now(timezone.utc).isoformat()

        # Save the modified content back to the processed data directory
        output_path = PROCESSED_DATA_PATH / file
        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(content, outfile, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    # Run the preprocessing function
    preprocess()
