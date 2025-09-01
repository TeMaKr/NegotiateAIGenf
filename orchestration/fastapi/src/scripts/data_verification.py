import json
import logging
from datetime import datetime
from pathlib import Path

from pydantic import AnyHttpUrl, BaseModel, ValidationError


# Configure logging to write to both console and file
def setup_logging():
    """Set up logging to write to both console and file.
    This function creates a logger that writes logs to a file with a timestamp
    and also outputs logs to the console. The log file is created in the 'data/logs' directory.
    The log format includes a header line with the log level,
    ensuring it is exactly 70 characters long.
    Returns:
        logger (logging.Logger): Configured logger instance.
    """
    log_dir = Path(__file__).parent.parent / "data" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"data_verification_{timestamp}.txt"

    # Create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create custom formatter that ensures first line is exactly 70 characters
    class CustomFormatter(logging.Formatter):
        def format(self, record):
            # Create the header line with levelname, ensuring it's exactly 70 characters
            level_name = record.levelname
            header = f"----------------------- {level_name} -----------------------"
            # Pad or truncate to exactly 70 characters
            header = header[:70].ljust(70, "-")

            # Create the main log message
            formatted_message = super().format(record)

            return f"{header}\n{formatted_message}"

    formatter = CustomFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()

path = Path(__file__).parent.parent / "data"
PROCESSED_DATA_PATH = path / "processed"
TAXONOMY_PATH = path / "taxonomies"
VALID_DOCUMENT_TYPES = {"statement", "pre session submission", "insession document"}

# List of files to process
FILES = [
    "metadata_session_1.json",
    "metadata_session_2.json",
    "metadata_session_3.json",
    "metadata_session_4.json",
    "metadata_session_5.json",
]

# Number of submissions expected for each session
NUM_SUBMISSIONS = {
    "1": 117,
    "2": 193,
    "3": 667,
    "4": 612,
    "5.1": 308,
}


def import_file(input_file_path: Path) -> dict | list:
    """Import a JSON file from the raw data directory."""
    with open(input_file_path, "r") as file:
        return json.load(file)


def extract_submissions(content: dict) -> list[dict]:
    """Extract submission information from the content."""
    return content.get("submissions", [])


def verify_topics(submissions: list[dict]) -> bool:
    """Verify that all submissions have a correct topic.
    This function checks if each submission has a topic that is present in the taxonomy file.
    It also checks for missing topics and topics that are not in the taxonomy.
    It raises a ValueError if the taxonomy file is not found or is not a list.
    Args:
        submissions (list[dict]): List of submissions to verify.
    Returns:
        bool: True if all submissions have a correct topic, False otherwise.
    Raises:
        ValueError: If the taxonomy file is not found or is not a list."""
    session = submissions[0].get("session", "")
    if session in ["1", "2"]:
        return True
    verified = True
    topics = import_file(TAXONOMY_PATH / "topics.json")
    if not topics:
        raise ValueError("No topics found in the taxonomy file.")
    if not isinstance(topics, list):
        raise ValueError("Topics taxonomy should be a list.")
    topics_set = {topic["category"] for topic in topics if "category" in topic}
    # unnest subcategories from topics as comprehension
    topics_set.update(
        subcategory
        for topic in topics
        if "subcategories" in topic
        for subcategory in topic["subcategories"]
    )

    counter_missing = 0
    counter_possibly_missing = 0
    missing_topics: set[str] = set()
    possibly_missing_topics: set[str] = set()
    counter_not_in_taxonomy = 0
    not_in_taxonomy_dict: dict[str, str] = {}
    for submission in submissions:
        if "topic" not in submission or not submission["topic"]:
            if submission.get("document_type") == "statement":
                counter_possibly_missing += 1
                possibly_missing_topics.add(submission["href"])
                continue
            counter_missing += 1
            missing_topics.add(submission["href"])
            continue
        for topic in submission["topic"]:
            if topic not in topics_set:
                counter_not_in_taxonomy += 1
                not_in_taxonomy_dict[submission["href"]] = topic

    if counter_missing > 0:
        msg = "submission is" if counter_missing == 1 else "submissions are"
        logger.warning(
            f"Session {session} - missing\n"
            f"{counter_missing} {msg} missing a topic.\n"
            f"{'\n'.join(missing_topics)}"
        )

    if counter_possibly_missing > 0:
        msg = "submission is" if counter_possibly_missing == 1 else "submissions are"
        logger.warning(
            f"Session {session} - possibly missing\n"
            f"{counter_possibly_missing} {msg} possibly missing a topic (document type 'statement').\n"
            f"{'\n'.join(possibly_missing_topics)}"
        )

    if counter_not_in_taxonomy > 0:
        msg = "submission has" if counter_not_in_taxonomy == 1 else "submissions have"
        logger.error(
            f"Session {session} - not in taxonomy\n"
            f"{counter_not_in_taxonomy} {msg} topics not in the taxonomy:\n"
            f"{'\n'.join(f'{href}: {topic}' for href, topic in not_in_taxonomy_dict.items())}"
        )
        verified = False

    return verified


def verify_authors(submissions: list[dict]) -> bool:
    """Verify that all submissions have a correct author.
    This function checks if each submission has an author that is present in the taxonomy file.
    It also checks for missing authors and authors.
    It raises a ValueError if the taxonomy file is not found or is not a dictionary.
    Args:
        submissions (list[dict]): List of submissions to verify.
    Returns:
        bool: True if all submissions have a correct author, False otherwise.
    Raises:
        ValueError: If the taxonomy file is not found or is not a dictionary.
    """
    verified = True
    authors = import_file(TAXONOMY_PATH / "authors.json")
    if not authors:
        raise ValueError("No authors found in the taxonomy file.")
    if not isinstance(authors, dict):
        raise ValueError("Authors taxonomy should be a dictionary.")

    author_set = set(authors["members"]) if "members" in authors else set()
    country_associations = authors.get("country_associations", [])
    author_set.update(
        author["name"] for author in country_associations if "name" in author
    )
    author_set.update(
        member
        for author in country_associations
        for member in author["members"]
        if "members" in author
    )

    counter_missing = 0
    missing_authors: set[str] = set()
    counter_not_in_taxonomy = 0
    not_in_taxonomy_set: dict[str, str] = {}
    session = submissions[0].get("session", "")
    for submission in submissions:
        if "author" not in submission or not submission["author"]:
            counter_missing += 1
            missing_authors.add(submission["href"])
            continue
        else:
            for author in submission["author"]:
                if author not in author_set:
                    counter_not_in_taxonomy += 1
                    not_in_taxonomy_set[submission["href"]] = author
    if counter_missing > 0:
        msg = "submission is" if counter_missing == 1 else "submissions are"
        logger.error(
            f"Session {session} - missing\n"
            f"{counter_missing} {msg} missing an author.\n"
            f"{'\n'.join(missing_authors)}"
        )
        verified = False
    if counter_not_in_taxonomy > 0:
        msg = "submission has" if counter_not_in_taxonomy == 1 else "submissions have"
        logger.error(
            f"Session {session} - not in taxonomy\n"
            f"{counter_not_in_taxonomy} {msg} author(s) not in the taxonomy:\n"
            f"{'\n'.join(f'{href}: {author}' for href, author in not_in_taxonomy_set.items())}"
        )
        verified = False
    return verified


def verify_titles(submissions: list[dict]) -> bool:
    """Verify that all submissions have a correct title.
    This function checks if each submission has a title that is not empty and is a string.
    It also checks for missing titles and titles that are not valid strings.
    Args:
        submissions (list[dict]): List of submissions to verify.
    Returns:
        bool: True if all submissions have a correct title, False otherwise.
    """
    verified = True
    counter_missing = 0
    missing_titles: set[str] = set()
    session = submissions[0].get("session", "")
    title_not_valid: dict[str, str] = {}
    for submission in submissions:
        if (
            "title" not in submission
            or not submission["title"]
            or not str(submission["title"]).strip()
        ):
            counter_missing += 1
            missing_titles.add(submission["href"])
            continue
        if not isinstance(submission["title"], str):
            title_not_valid[submission["href"]] = submission["title"]
            continue

    if counter_missing > 0:
        msg = "submission is" if counter_missing == 1 else "submissions are"
        logger.error(
            f"Session {session} - missing\n"
            f"{counter_missing} {msg} missing a title.\n"
            f"{'\n'.join(missing_titles)}"
        )
        verified = False

    if title_not_valid:
        msg = "submission has" if len(title_not_valid) == 1 else "submissions have"
        logger.error(
            f"Session {session} - not valid\n"
            f"{len(title_not_valid)} {msg} an invalid title:\n"
            f"{'\n'.join(f'{href}: {title}' for href, title in title_not_valid.items())}"
        )
        verified = False

    return verified


def verify_for_duplicates(submissions: list[dict]) -> bool:
    verified = True
    session = submissions[0].get("session", "")
    titles: set = set()
    duplicates = []
    for submission in submissions:
        title = submission["title"]
        if title in titles:
            duplicates.append((submission["href"], title))
        titles.add(title)

    if duplicates:
        logger.error(
            f"Session {session} - duplicates found\n"
            f"The following submissions have duplicate titles:\n"
            f"{'\n'.join(f'{href}: {title}' for href, title in duplicates)}"
        )
    return verified


def verify_document_types(submissions: list[dict]) -> bool:
    """Verify that all submissions have a correct document type.
    This function checks if each submission has a document type
    that is present in the predefined set of valid document types.
    It also checks for missing document types and document types that are not in the taxonomy.
    Args:
        submissions (list[dict]): List of submissions to verify.
    Returns:
        bool: True if all submissions have a correct document type, False otherwise.
    """
    verified = True
    counter_missing = 0
    missing_types: set[str] = set()
    counter_not_in_taxonomy = 0
    not_in_taxonomy_set: dict[str, str] = {}
    session = submissions[0].get("session", "")
    for submission in submissions:
        if "document_type" not in submission or not submission["document_type"]:
            counter_missing += 1
            missing_types.add(submission["href"])
            continue
        else:
            document_type = submission["document_type"]
            if not isinstance(document_type, str):
                counter_not_in_taxonomy += 1
                not_in_taxonomy_set[submission["href"]] = document_type
            else:
                # Here you would check against a predefined set of valid document types
                if document_type not in VALID_DOCUMENT_TYPES:
                    counter_not_in_taxonomy += 1
                    not_in_taxonomy_set[submission["href"]] = document_type

    if counter_missing > 0:
        msg = "submission is" if counter_missing == 1 else "submissions are"
        logger.error(
            f"Session {session} - missing\n"
            f"{counter_missing} {msg} missing a document type.\n"
            f"{'\n'.join(missing_types)}"
        )
        verified = False
    if counter_not_in_taxonomy > 0:
        # Log the document types not in the taxonomy plus their submission hrefs
        msg = "submission has" if counter_not_in_taxonomy == 1 else "submissions have"
        logger.error(
            f"Session {session} - invalid\n"
            f"{counter_not_in_taxonomy} {msg} an invalid document type:\n"
            f"{'\n'.join(f'{href}: {doc_type}' for href, doc_type in not_in_taxonomy_set.items())}"
        )
        verified = False
    return verified


def verify_submission_numbers(submissions: list[dict]) -> bool:
    """Verify that the number of submissions is consistent across all files.
    This function checks if the number of submissions matches the expected count
    for the given session. It raises a ValueError if the session is not valid or
    if the expected count is not found.
    Args:
        submissions (list[dict]): List of submissions to verify.
    Returns:
        bool: True if the number of submissions matches the expected count, False otherwise.
    Raises:
        ValueError: If the session is not valid or if the expected count is not found.
    """
    if not submissions:
        raise ValueError("No submissions found.")

    session = submissions[0].get("session", "")
    if not session or isinstance(session, list):
        raise ValueError(f"Invalid session value: {session}.")

    submission_count = len(submissions)

    expected_count = NUM_SUBMISSIONS.get(session, None)
    if expected_count is None:
        logger.error(
            f"Session {session} - not valid\n"
            f"No expected submission count found for session {session}."
        )
        return False

    if expected_count != submission_count:
        logger.error(
            f"Session {session} - not valid\n"
            f"Expected {expected_count} submissions, but found {submission_count}."
        )
        return False

    return True


class TestModel(BaseModel):
    """Test model for verifying hrefs."""

    href: AnyHttpUrl


def verify_hrefs(submissions: list[dict]) -> bool:
    """Verify that all hrefs in submissions are valid URLs and unique.
    This function checks if each submission has a valid href that is a URL.
    It also checks for missing hrefs, duplicate hrefs, and invalid hrefs.
    Args:
        submissions (list[dict]): List of submissions to verify.
    Returns:
        bool: True if all hrefs are valid, unique, and no hrefs are missing, False otherwise.
    """
    verified = True
    seen: set[str] = set()
    missing_count = 0
    duplicates: dict[str, int] = {}
    invalid_hrefs: set[str] = set()
    session = submissions[0].get("session", "")
    for submission in submissions:
        href = submission.get("href")
        if not href:
            # Add a unique identifier for submissions without href
            missing_count += 1
            continue
        # Check if href is a valid URL
        try:
            test_model = TestModel(href=href)
            TestModel.model_validate(test_model)
        except ValidationError:
            invalid_hrefs.add(href)
        # Check if href is already seen
        if href in seen:
            if href in duplicates:
                duplicates[href] += 1
            else:
                duplicates[href] = 1
        else:
            seen.add(href)
    sum_duplicates = sum(duplicates.values())

    if duplicates:
        msg = "href" if sum_duplicates == 1 else "hrefs"
        logger.error(
            f"Session {session} - not valid\n"
            f"{sum_duplicates} duplicate {msg}:\n"
            f"{'\n'.join(f'{href}: {count}' for href, count in duplicates.items())}"
        )
        verified = False

    if missing_count > 0:
        msg = "submission is" if missing_count == 1 else "submissions are"
        logger.error(
            f"Session {session} - missing\n{missing_count} {msg} missing an href."
        )
        verified = False

    if invalid_hrefs:
        msg = "href" if len(invalid_hrefs) == 1 else "hrefs"
        logger.error(
            f"Session {session} - invalid\n"
            f"{len(invalid_hrefs)} {msg} not valid:\n"
            f"{'\n'.join(invalid_hrefs)}"
        )
        verified = False

    return verified


def verify() -> bool:
    """Run all verification scripts in the correct order.
    This function imports the necessary files, extracts submissions,
    and verifies each submission against the defined criteria.
    It logs the results of each verification step and returns True if all verifications passed,
    or False if any verification failed.
    Args:
        None
    Returns:
        bool: True if all verifications passed, False otherwise.
    Raises:
        ValueError: If any submission is invalid or if the content is not a dictionary.
    """
    verified_all = True
    for file in FILES:
        input_file_path = PROCESSED_DATA_PATH / file
        content = import_file(input_file_path)
        if not content or not isinstance(content, dict):
            raise ValueError(f"Invalid content in {file}. Expected a dictionary.")
        submissions = extract_submissions(content)

        verified_session = all(
            [
                verify_topics(submissions),
                verify_authors(submissions),
                verify_titles(submissions),
                verify_document_types(submissions),
                verify_submission_numbers(submissions),
                verify_hrefs(submissions),
                verify_for_duplicates(submissions),
            ]
        )

        if verified_session:
            logger.info(f"All verifications passed for {file}.")
        else:
            verified_all = False
    if verified_all:
        logger.info("All verifications passed for all files.")
    else:
        logger.error("Some verifications failed. Please check the logs for details.")
    return verified_all
