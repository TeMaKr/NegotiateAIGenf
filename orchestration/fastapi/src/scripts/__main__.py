import logging

from scripts.create_collections import create_collections
from scripts.preprocess_authors import preprocess as preprocess_authors
from scripts.preprocess_titles import preprocess as preprocess_titles
from scripts.preprocess_topics import preprocess as preprocess_topics
from scripts.seed_database import seed_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Preprocessing has to start with the authors, then topics, and finally titles.


def main():
    scripts = [
        preprocess_authors,
        preprocess_topics,
        preprocess_titles,
        create_collections,
        seed_database,
    ]

    for script in scripts:
        try:
            logger.info(f"Starting script: {script.__name__}")
            script()
            logger.info(f"Script {script.__name__} completed successfully.")
        except Exception as e:
            logger.error(f"Error running script {script.__name__}: {e}")
            raise


if __name__ == "__main__":
    main()
