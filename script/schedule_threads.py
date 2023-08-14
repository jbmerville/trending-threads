import logging.config
from config.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from script.scheduler.event_scheduler import EventScheduler


def main(file_names):
    try:
        logger.info("=== Starting schedule threads process ===")

        event_scheduler = EventScheduler(30)
        event_scheduler.schedule_events(file_names)

        logger.info(f"Finished process")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise e


if __name__ == "__main__":
    main(["Cristiano_Ronaldo", "Meteor_shower", "Tom_Jones", "Barack_Obama"])
