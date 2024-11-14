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

    def sync_with_google(self):
        pass

    def sync_with_office365(self):
        pass

    def sync_with_file(self, file_path):
        pass

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
    c.sync_with_office365()
    c.sync_with_file("some-file/path/calendar.ics")
    c.save()
