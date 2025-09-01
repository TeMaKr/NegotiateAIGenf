# TODO: change to new setup

import logging

from tasks import fetch_previous, synchronize

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def import_session_5_1() -> str:
    """
    Import previous session 5.1 data into the database.
    """
    task = synchronize.delay(
        base_url="https://www.unep.org/inc-plastic-pollution/session-5/documents/in-session"
    )
    return task.id


def import_previous() -> str:
    """
    Import previous sessions data into the database.
    """
    task = fetch_previous.delay()
    return task.id
