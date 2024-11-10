# settings

* create app

```sh
python manage.py startapp chat
```


* Create templates

```sh
mkdir -p chat/templates/chat
```

* super user

```bash
$ python manage.py createsuperuser

Username (leave blank to use 'foo'): admin
Email address: fakse@foo.com
Password:
Password (again):
The password is too similar to the username.
This password is too short. It must contain at least 8 characters.
This password is too common.
Bypass password validation and create user anyway? [y/N]: y
Superuser created successfully.
```

* update settings

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'chat',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles'
]
```

* update storage details

```python
def chatbot():
    return ChatBot(
        'Trainer',
        storage_adapter='chatterbot.storage.SQLStorageAdapter',
        database_uri='sqlite:///chatbot.sqlite3'
    )
```


* default view

```python
from django.http import HttpResponse


def main_view(request):
    return HttpResponse("hello world")
```

* query

```python
from django.http import HttpResponse
from chatbot import chatbot


def chat_query(request):
    user_message = request.GET['message']
    response = chatbot().get_response(user_message)
    response_data = response.text
    return HttpResponse(response_data)
```

* URLs in chat app

> chat/urls.py


```python
from django.urls import path

from . import views

urlpatterns = [
    path('query', views.chat_query, name='chat_query'),
]
```

* test query

```bash
curl "http://localhost:8000/chat/query?message=hi"
```

* response

```bash
*   Trying 127.0.0.1:8000...
* Connected to localhost (127.0.0.1) port 8000 (#0)
> GET /chat/query?message=hi HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/7.85.0
> Accept: */*
>
* Mark bundle as not supporting multiuse
< HTTP/1.1 200 OK
< Date: Sun, 01 Jan 2023 18:00:26 GMT
< Server: WSGIServer/0.2 CPython/3.7.9
< Content-Type: text/html; charset=utf-8
< X-Frame-Options: DENY
< Content-Length: 12
< X-Content-Type-Options: nosniff
< Referrer-Policy: same-origin
<
* Connection #0 to host localhost left intact
How are you?
```

# template

> chat/templates/chat/main.html

content

```html
<!doctype html>
<html lang="en" class="scroll-smooth">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Chatbot demo</title>
    </head>
  <body>
    <p>hello world!</p>
</body>
</html>
```

