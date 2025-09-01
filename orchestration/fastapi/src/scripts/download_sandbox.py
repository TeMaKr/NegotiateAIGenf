import json
import logging
from pathlib import Path

from scraper.helper import fetch_response

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

path = Path(__file__).parent / "data"
PROCESSED_DATA_PATH = path / "processed"

FILES = [
    "metadata_session_1.json",
    "metadata_session_2.json",
    "metadata_session_3.json",
    "metadata_session_4.json",
    "metadata_session_5.json",
]


def import_file(input_file_path: Path) -> dict:
    """Import a JSON file from the raw data directory.
    Args:
        filename (str): The name of the JSON file to import.
    Returns:
        dict: The content of the JSON file as a dictionary.
    Raises:
        FileNotFoundError: If the specified file does not exist in the raw data directory.
    """
    with open(input_file_path, "r") as file:
        return json.load(file)


def download_file(file_url: str) -> bytes | None:
    """Downloads a file from the given URL.
    Args:
        file_url (str): The URL of the file to download.
    Returns:
        bytes | None: The content of the file if successful, None otherwise.
    """
    if not file_url:
        return None
    # Remove query parameters from the URL if they exist
    file_url = file_url.split("?")[0]
    # Remove pound sign and everything after it
    file_url = file_url.split("#")[0]
    if not file_url.endswith(".pdf"):
        return None
    pdf_response = fetch_response(file_url, retries=3)
    if pdf_response:
        return pdf_response.content
    return None


def validate_downloads(
    output_file_path: Path = PROCESSED_DATA_PATH / "downloads",
) -> None:
    """Validate the downloaded files.
    Args:
        output_file_path (Path): The path to the output directory.
    """
    for file_name in FILES:
        output_file_path_session = output_file_path / (file_name.split(".")[0])
        output_file_path_session.mkdir(parents=True, exist_ok=True)
        file_list = [file.name for file in output_file_path_session.glob("**/*.pdf")]
        input_file_path = PROCESSED_DATA_PATH / file_name
        content = import_file(input_file_path)
        submissions = content.get("submissions", [])
        for submission in submissions:
            file_url = submission.get("href", "")
            file_url = file_url.split(".pdf")[0]
            filename = f"{file_url.split('/')[-1]}.pdf"
            if filename not in file_list:
                logger.warning(f"Missing file: {filename}")


def main():
    """Main function to download sandbox files."""
    output_file_path = PROCESSED_DATA_PATH / "downloads"
    output_file_path.mkdir(parents=True, exist_ok=True)
    for file_name in FILES:
        output_file_path_session = output_file_path / (file_name.split(".")[0])
        output_file_path_session.mkdir(parents=True, exist_ok=True)
        input_file_path = PROCESSED_DATA_PATH / file_name
        if not input_file_path.exists():
            continue
        content = import_file(input_file_path)
        submissions = content.get("submissions", [])
        for submission in submissions:
            file_url = submission.get("href", "")
            file_url_str = file_url.split(".pdf")[0]
            file_name = f"{file_url_str.split('/')[-1]}.pdf"
            output_file = output_file_path_session / file_name
            if not file_url:
                raise ValueError(f"File URL: {file_url}")
            file_content = download_file(file_url)
            if file_content is None:
                continue
            with open(output_file, "wb") as output_file:
                output_file.write(file_content)
        logger.info(f"Downloaded and saved files from {file_name}.")  # type: ignore


if __name__ == "__main__":
    main()
    validate_downloads()

"""
Tod tar and compress the downloaded files:

cd orchestration/fastapi/src/data/processed/downloads
for d in */ ; do tar -czf "${d%/}.tar.gz" "$d"; done

"""
