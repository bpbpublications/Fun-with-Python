# train


## install

```sh
pip install chatterbot
```

```sh
$ pip install spacy==3.4.4 pyyaml==5.4.1
$ git clone git@github.com:bpbpublications/Fun-with-Python.git
$ cd fun-with-Python/chapter_3/ChatterBot/
$ python setup.py install
```

## fix

With proper dicitonary loading

```sh
pip install git+git://github.com/code4tag/ChatterBot.git@1.0.8.en_patch
```

install module

```sh
python -m spacy download en
```

# training model

```sh
mkdir -p ~/chatterbot_corpus/data/english
```

create training file

```sh
vim ~/chatterbot_corpus/data/english/conversations.yml
```

```yaml
categories:

- conversations
  conversations:
- - Good morning, how are you?
  - I am doing well, how about you?
  - I'm also good.
  - That's good to hear.
  - Yes it is.
- - Hello
  - Hi
  - How are you doing?
  - I am doing well.
  - That is good to hear
  - Yes it is.
  - Can I help you with anything?
  - Yes, I have a question.
  - What is your question?
  - Could I borrow a cup of sugar?
  - I'm sorry, but I don't have any.
  - Thank you anyway
  - No problem
- - How are you doing?
  - I am doing well, how about you?
  - I am also good.
  - That's good.
- - Have you heard the news?
  - What good news?
- - What is your favorite book?
  - I can't read.
  - So what's your favorite color?
  - Blue
```

# interact

simple question

```python
response = _chatbot.get_response('how are you?')
print(response)
```

Basic conversation

```python
In [1]: from chatbot import chatbot

In [2]: c=chatbot()

In [3]: c.get_response('hi')
Out[3]: <Statement text:How are you doing?>

In [4]: print(c.get_response('hi'))
How are you doing?

In [5]: print(c.get_response('how are you?'))
I am doing well.
```

# django

```sh
pip install django
```

initialize

```sh
django-admin startproject chatter
```

expected

```sh
.
├── chatter
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
└── manage.py
```

running main

```sh
$ python manage.py runserver

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 30, 2022 - 09:44:56
Django version 3.2.16, using settings 'chatter.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

* applly migrations

```sh
$ python manage.py migrate

Operations to perform:
Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
Applying contenttypes.0001_initial... OK
Applying auth.0001_initial... OK
Applying admin.0001_initial... OK
Applying admin.0002_logentry_remove_auto_add... OK
Applying admin.0003_logentry_add_action_flag_choices... OK
Applying contenttypes.0002_remove_content_type_name... OK
Applying auth.0002_alter_permission_name_max_length... OK
Applying auth.0003_alter_user_email_max_length... OK
Applying auth.0004_alter_user_username_opts... OK
Applying auth.0005_alter_user_last_login_null... OK
Applying auth.0006_require_contenttypes_0002... OK
Applying auth.0007_alter_validators_add_error_messages... OK
Applying auth.0008_alter_user_username_max_length... OK
Applying auth.0009_alter_user_last_name_max_length... OK
Applying auth.0010_alter_group_name_max_length... OK
Applying auth.0011_update_proxy_permissions... OK
Applying auth.0012_alter_user_first_name_max_length... OK
Applying sessions.0001_initial... OK
```

* start app

```sh
python manage.py startapp chat
```
