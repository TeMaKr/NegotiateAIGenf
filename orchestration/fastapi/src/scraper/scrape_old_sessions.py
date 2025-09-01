import json
from pathlib import Path

from models.submissions import Metadata
from scraper.helper import UNEPMetadata, _post_process_metadata, write_metadata_to_file
from scraper.session_1_processing import scrape as scraper_1
from scraper.session_2_processing import scrape as scraper_2
from scraper.session_3_processing import scrape as scraper_3
from scraper.session_4_processing import scrape as scraper_4
from scraper.session_5_scraping import get_current_submissions as scraper_5
from settings import settings

SESSION_JSON_PATH = Path(__file__).parent / "sessions.json"


def get_old_submissions() -> list[Metadata]:
    """Main function to run the scraper."""
    with open(SESSION_JSON_PATH, "r", encoding="utf-8") as f:
        session_data = json.load(f)
    # Initialize an empty list to store metadata (Metadata) objects
    metadata_list: list[Metadata] = []
    # Define a mapping of session numbers to their respective scraper functions
    scraper_mapping = {
        "1": scraper_1,
        "2": scraper_2,
        "3": scraper_3,
        "4": scraper_4,
    }
    for session, document_types in session_data.items():
        # Initialize an empty list for the current session's metadata
        metadata_list_session: list[UNEPMetadata] = []
        # Check if the session exists in the scraper mapping
        if session in scraper_mapping.keys():
            # Iterate over each document type configuration for the session
            for _, config in document_types.items():
                # Run the scraper function for the session and document type
                metadata_list_session.extend(
                    [
                        metadata
                        for metadata in scraper_mapping[session](
                            base_url=config["base_url"],
                            accordion_names=config["accordionnames"],
                            session=session,
                            document_type=config.get("document_type", None),
                        )
                    ]
                )
            # deduplicate metadata_list_session based on href
            seen_hrefs = set()
            metadata_list_session = [
                metadata
                for metadata in metadata_list_session
                if metadata.file not in seen_hrefs and not seen_hrefs.add(metadata.file)
            ]
            # if settings.environment.environment == "LOCAL":
            metadata_post_process = [
                _post_process_metadata(metadata, session=session)
                for metadata in metadata_list_session
            ]
            write_metadata_to_file(
                session=session,
                metadata_list=metadata_post_process,
            )
            metadata_list.extend(metadata_post_process)

    session_5_1_metadata = scraper_5(
        base_url="https://www.unep.org/inc-plastic-pollution/session-5/documents/in-session"
    )

    write_metadata_to_file(
        session="5",
        metadata_list=session_5_1_metadata,
    )
    return metadata_list


if __name__ == "__main__":
    get_old_submissions()
