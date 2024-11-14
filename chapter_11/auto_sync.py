import time
import coloredlogs
import logging
from os import path
from manage_full import SYNC_FILE
from manage_full import MyCalendar

MAX_FILE_TTL = 3


def check_file_ttl():
    if path.exists(SYNC_FILE):
        file_ttl = (time.time() - path.getmtime(SYNC_FILE)) / 60  # in minutes
        logging.debug(file_ttl)
        if file_ttl >= MAX_FILE_TTL:
            logging.info("Cleaning up and syncing calendar events to main calendar service...")
            cal = MyCalendar()
            cal.push_events_to_google()
    else:
        logging.warning(f"Sync evenets file {SYNC_FILE} does not exists yet, taking nap...")
    logging.warning(f"Not much to do at the moment, taking nap...")
    time.sleep(10)


if __name__ == "__main__":
    coloredlogs.install(level=logging.DEBUG)
    while True:
        check_file_ttl()
