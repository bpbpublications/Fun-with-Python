import coloredlogs
import logging
import os
import pytz
from datetime import datetime
from icalendar import Calendar, Event
from gcsa.google_calendar import GoogleCalendar

CALENDAR_FILE = "/var/tmp/calendar.ics"


class MyCalendar:
    cal = None

    def __init__(self):
        self.read()
        if not self.cal:
            self.cal = Calendar()
            self.cal.add("prodid", "-//My calendar product//mxm.dk//")
            self.cal.add("version", "2.0")
        self.gc = GoogleCalendar()

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
        credentials = (client_id, secret_id)
        protocol = MSGraphProtocol()
        scopes = ["https://graph.microsoft.com/.default"]
        account = Account(credentials, protocol=protocol)
        if not account.is_authenticated:
            if account.authenticate(scopes=scopes):
                print("Authenticated")
        schedule1 = account.schedule(resource=f"{user}@hotmail.com")
        calendar1 = schedule1.get_default_calendar()
        for event in calendar1.get_events(include_recurring=False):
            component = self.find_event(event.summary, event.start)
            if not component:
                record = {
                    "summary": event.subject,
                    "dtstart": event.start,
                    "dtend": event.end,
                    "dtstamp": event.created,
                    "uid": event.object_id,
                }
                record = self.create_event(record)
                logging.info(f"Adding calendar record to database")
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
                and component.get("name") == event_name
                and component.decoded("dtstart") == event_start
            ):
                return component

    def read(self):
        if os.path.exists(CALENDAR_FILE):
            with open(CALENDAR_FILE, "rb") as f:
                self.cal = Calendar.from_ical(f.read())

    def save(self):
        with open(CALENDAR_FILE, "wb") as f:
            f.write(self.cal.to_ical())


if __name__ == "__main__":
    coloredlogs.install(level=logging.DEBUG)
    c = MyCalendar()
    c.sync_with_google()
    c.save()
