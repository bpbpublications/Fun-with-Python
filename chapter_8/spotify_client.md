# install

```sh
$ pip install gunicorn==20.1.0
$ pip install fastapi==0.96.0
```


* spotify

```sh
$ pip install git+https://github.com/darkman66/spotify.py.git
```

# run

* example 1
```sh
$ gunicorn -k uvicorn.workers.UvicornWorker spotify_client:app --reload -b localhost:8888
```

bug in spotify code

https://github.com/mental32/spotify.py/pull/68

## API auth test

```sh
curl -X POST "https://accounts.spotify.com/api/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "grant_type=client_credentials&client_id=< your client id >&client_secret=< your client secret >"

# response
{"access_token":"***","token_type":"Bearer","expires_in":3600}
```
* test

```sh
$ curl -v http://localhost:8888/

*   Trying 127.0.0.1:8888...
* Connected to 127.0.0.1 (127.0.0.1) port 8888 (#0)
> GET / HTTP/1.1
> Host: 127.0.0.1:8888
> User-Agent: curl/7.88.1
> Accept: */*
>
< HTTP/1.1 200 OK
< date: Sat, 17 Jun 2023 19:24:02 GMT
< server: uvicorn
< content-length: 33
< content-type: application/json
<
* Connection #0 to host 127.0.0.1 left intact

{"url":"http://foo.com/redirect"}
```

* credentials

```ini
[spotify]
client_id = <your client ID>
client_secret = <your client secret>
```

# start app

## example 1

```sh
$ gunicorn -k uvicorn.workers.UvicornWorker api_step1:app --reload -b localhost:8888
```
## example 2

```sh
$ gunicorn -k uvicorn.workers.UvicornWorker api_step2:app --reload -b localhost:8888
```
## example 3

```sh
$ gunicorn -k uvicorn.workers.UvicornWorker api_step3:app --reload -b localhost:8888
```

* callback

```
http://localhost:8888/spotify/callback?code=<..authentication code..>
```

* response

```json
{"url":"https://open.spotify.com/track/7aRCf5cLOFN1U7kvtChY1G"}
```

# search

```sh
$ curl -v -X POST http://localhost:8888/search/ -H 'content-type: application/json' -d '{"phrase" : "linking park"}'
```
## search modified

```python
@app.post("/search/")
async def spotify_search(item: Item):
    async with spotify.Client(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) as client:
        results = await client.search(item.phrase)
        if results.tracks and len(results.tracks) > 0:
            track_url = results.tracks[0].url
            track_id = track_url.split('/')[-1]
    return {
        "track_url": track_url,
        "ID": track_id
    }
```

# play track

```python
@app.get("/play/{track_id}")
async def spotify_playback(track_id: str):
     code = await token()
     async with spotify.Client(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) as client:
          response = await spotify.User.from_code(client, code, redirect_uri=REDIRECT_URI)
          user = await response
          devices = await user.get_devices()
          device_id = devices[0].id
          p = await user.get_player()'
          play_url  = f"https://open.spotify.com/track/{track_id}"
          await p.play(play_url, device_id)
```

# with httpx

```python
import httpx

@app.post("/play/{track_id}")
async def spotify_play(track_id: str):
    r = httpx.post('https://httpbin.org/post', data={'key': 'value'})
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = f"grant_type=client_credentials&client_id={SPOTIFY_CLIENT_ID}&client_secret={SPOTIFY_CLIENT_SECRET}"
        response = await client.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        access_token = response.json()['access_token']

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        data = {'context_uri': f"spotify:track:{track_id}"}
        response = await client.put("https://api.spotify.com/v1/me/player/play", headers=headers, data=data)
        print(response.content)
```

# with browser

```python
import webbrowser

@app.post("/play/{track_id}")
async def spotify_play(track_id: str):
     play_url  = f"https://open.spotify.com/track/{track_id}"
     webbrowser.open(play_url)
```


# headless

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True

driver = webdriver.Chrome(options=options)
driver.get('https://www.wikipedia.org')

# close once finished
driver.close()
```
