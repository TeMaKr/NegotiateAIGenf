"""Note this script is for testing purposes only and should not be used in production!"""

import logging
import time

import httpx

from scripts.data_verification import verify
from scripts.import_authors import import_authors
from scripts.import_session_data import import_session_data
from scripts.import_topics import import_topics
from settings import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for health check configuration
MAX_RETRIES = 10
RETRY_DELAY = 25
HEALTH_CHECK_TIMEOUT = 10


def wait_for_api_health() -> bool:
    """
    Wait for FastAPI to become healthy with retry logic.

    Returns:
        bool: True if API is healthy, False if max retries exceeded
    """

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = httpx.get(
                f"{settings.fastapi_api.host}/api/ping",
                timeout=HEALTH_CHECK_TIMEOUT,
            )
            response.raise_for_status()
            logger.info("FastAPI is healthy.")
            return True
        except httpx.RequestError as e:
            logger.warning(f"Attempt {attempt}/{MAX_RETRIES}: Connection error - {e}")
        except httpx.HTTPStatusError as e:
            logger.warning(
                f"Attempt {attempt}/{MAX_RETRIES}: HTTP error - {e.response.status_code}"
            )
        except Exception as e:
            logger.warning(f"Attempt {attempt}/{MAX_RETRIES}: Unexpected error - {e}")
        if attempt < MAX_RETRIES:
            logger.info(f"Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)

    logger.error(f"FastAPI is not healthy after {MAX_RETRIES} retries. Exiting.")
    return False


def seed_database():
    if wait_for_api_health():
        import_authors()
        import_topics()
        if not verify():
            logger.error("Data verification failed. Exiting.")
            raise RuntimeError("Data verification failed.")
        logger.info("Data verification passed. Proceeding to import session data.")
        import_session_data()
    else:
        logging.error("FastAPI did not become healthy in time. Exiting.")
