from gcsa.google_calendar import GoogleCalendar


gc = GoogleCalendar(credentials_path="/var/tmp/credentials.json")
for event in gc.get_events():
    print(event)
