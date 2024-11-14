import coloredlogs
import configparser
import logging
import os
import pytz
import pickle
from datetime import datetime
from icalendar import Calendar, Event
from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event as google_event
from O365 import Account, MSGraphProtocol

CALENDAR_FILE = "/var/tmp/calendar.ics"
SYNC_FILE = "/tmp/events_to_sync.bin"


class MyCalendar:
    cal = None

    def __init__(self):
        self.read()
        if not self.cal:
            self.cal = Calendar()
            self.cal.add("prodid", "-//My calendar product//mxm.dk//")
            self.cal.add("version", "2.0")
        self.gc = GoogleCalendar(credentials_path=self.settings["google"]["credentials_path"])

    @property
    def account(self):
        credentials = (self.settings["office365"]["client_id"], self.settings["office365"]["secret_id"])
        protocol = MSGraphProtocol()
        scopes = ["https://graph.microsoft.com/.default"]
        account = Account(credentials, protocol=protocol)
        if not account.is_authenticated:
            if account.authenticate(scopes=scopes):
                logging.info("Office 365 Authenticated")
        return account

    @property
    def settings(self):
        if not hasattr(self, "_config"):
            self._config = configparser.ConfigParser()
            self._config.read("sync.ini")
        return self._config

    def sync_with_google(self):
        for event in self.gc.get_events():
            component = self.find_event(event.summary, event.start)
            if not component:
                record = {
                    "summary": event.summary,
                    "dtstart": event.start,
                    "dtend": event.end,
                    "dtstamp": event.created,
                    "uid": event.event_id,
                }
                record = self.create_event(record)
                logging.info(f"Adding calendar record to database")
                self.cal.add_component(record)

    def sync_with_office365(self):
        user = self.settings["office365"]["user"]
        schedule1 = self.account.schedule(resource=f"{user}@hotmail.com")
        calendar1 = schedule1.get_default_calendar()
        for event in calendar1.get_events(include_recurring=False):
            component = self.find_event(event.subject, event.start)
            if not component:
                record = {
                    "summary": event.subject,
                    "dtstart": event.start,
                    "dtend": event.end,
                    "dtstamp": event.created,
                    "uid": event.object_id,
                }
                record = self.create_event(record)
                logging.info(f"Adding Office365 calendar record to database")
                self.cal.add_component(record)

    def sync_with_file(self):
        with open(self.settings["ics"]["path"], "rb") as f:
            calendar = Calendar.from_ical(f.read())
            for event in calendar.walk("VEVENT"):
                component = self.find_event(event["SUMMARY"], event["DTSTART"])
                if not component:
                    record = {
                        "summary": event["SUMMARY"],
                        "dtstart": event["DTSTART"],
                        "dtend": event["DTEND"],
                        "dtstamp": event["DTSTAMP"],
                        "uid": event["UID"],
                    }
                    record = self.create_event(record)
                    logging.info(f"Adding ics calendar record to database")
                    self.cal.add_component(record)

    def create_event(self, event_dict):
        event = Event()
        for k, v in event_dict.items():
            event.add(k, v)
        return event

    def find_event(self, event_name, event_start):
        for component in self.cal.walk():
            if (
                component.name.upper() == "VEVENT"
                and component.get("summary") == event_name
                and (component.get("dtstart") == event_start or component.decoded("dtstart") == event_start)
            ):
                logging.debug("Found item")
                return component

    def find_event_by_id(self, event_id):
        for component in self.cal.walk():
            if component.name.upper() == "VEVENT" and component.get("uid") == event_id:
                logging.debug("Found item")
                return component

    def read(self):
        if os.path.exists(CALENDAR_FILE):
            with open(CALENDAR_FILE, "rb") as f:
                self.cal = Calendar.from_ical(f.read())

    def save(self):
        with open(CALENDAR_FILE, "wb") as f:
            f.write(self.cal.to_ical())

    def push_events(self, new_events):
        logging.info(f"Number of events to push: {len(new_events)}")
        events_ids = [ev["UID"] for ev in new_events]
        with open(SYNC_FILE, "wb") as f:
            f.write(pickle.dumps(events_ids))

    def push_events_to_google(self):
        if os.path.exists(SYNC_FILE):
            with open(SYNC_FILE, "rb") as f:
                for item in pickle.loads(f.read()):
                    event = self.find_event_by_id(item)
                    if event:
                        ev = google_event(
                            event.get("SUMMARY", "untitled event"), start=event["DTSTART"], end=event["DTEND"]
                        )
                        self.gc.add_event(ev)
                    else:
                        logging.warning(f"Seems like event ID {item} is missing in calendar")
            os.unlink(SYNC_FILE)


if __name__ == "__main__":
    coloredlogs.install(level=logging.DEBUG)
    c = MyCalendar()
    c.sync_with_google()
    c.sync_with_office365()
    c.sync_with_file()
    c.save()
