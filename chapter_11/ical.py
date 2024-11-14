import icalendar


ics_file = "myevents.ics"
with open(ics_file, "rb") as f:
    calendar = icalendar.Calendar.from_ical(f.read())
    for event in calendar.walk("VEVENT"):
        print("-" * 10)
        print(event.get("name"))
        print(event.get("SUMMARY"))
