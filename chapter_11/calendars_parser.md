# packages

```bash
$ pip install pytz coloredlogs icalendar gcsa
```

# add event

```python
record = {
    "summary": event.summary,
    "dtstart": event.start,
    "dtend": event.end,
    "dtstamp": event.created,
    "uid": event.event_id
}
record = self.create_event(record)
```


# ics service

## install

```bash
$ pip install flask==3.0.0
```

## start service

```bash
$ flask --app ics_service run
 * Serving Flask app 'ics_service'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

# sync local calendar

```pythhon
127.0.0.1 - - [02/Jan/2024 14:35:06] "GET /calendar HTTP/1.1" 200 -
ERROR:ics_service:Exception on /calendar [PUT]
Traceback (most recent call last):
  (...)
  File "/Users/hubertpiotrowski/work/fun-with-python/chapter_11/manage_full.py", line 129, in push_events
    event["SUMMARY"],
  File "/Users/hubertpiotrowski/.virtualenvs/fun2/lib/python3.10/site-packages/icalendar/caselessdict.py", line 40, in __getitem__
    return super().__getitem__(key.upper())
KeyError: 'SUMMARY'
```
