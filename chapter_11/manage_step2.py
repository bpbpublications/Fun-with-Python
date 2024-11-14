def __init__(self):
    self.gc = GoogleCalendar(credentials_path="google_credentials.json")


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
