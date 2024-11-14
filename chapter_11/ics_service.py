import os
from flask import Flask, make_response, request
from icalendar import Calendar
from manage_full import CALENDAR_FILE, MyCalendar

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Calendar service</p>"


def read_calendar():
    if not os.path.exists(CALENDAR_FILE):
        cal = Calendar()
        cal.add("prodid", "-//My calendar product//mxm.dk//")
        cal.add("version", "2.0")
        resp = make_response(cal.to_ical(), 200)
        resp.headers["content-type"] = "text/calendar"
        return resp

    with open(CALENDAR_FILE, "rb") as f:
        resp = make_response(f.read(), 200)
        resp.headers["content-type"] = "text/calendar"
        return resp


@app.route("/calendar", methods=["GET"])
def calendar():
    return read_calendar()


@app.route("/calendar", methods=["PUT"])
def calendar_put():
    events_to_push = []
    cal = MyCalendar()
    new_calendar = Calendar.from_ical(request.data)
    for component in new_calendar.walk():
        if component.name.upper() == "VEVENT" and not cal.find_event_by_id(component.get("uid")):
            events_to_push.append(component)

    with open(CALENDAR_FILE, "wb") as f:
        f.write(request.data)

    # now we have to push to original calendar what we have added
    if events_to_push:
        cal = MyCalendar()
        cal.push_events(events_to_push)

    return read_calendar()
