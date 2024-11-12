import configparser
import httpx
import os
import spotify
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import Tuple

config = configparser.ConfigParser()
config.sections()
config.read("api_config.ini")

SPOTIFY_CLIENT_ID = config.get("spotify", "client_id")
SPOTIFY_CLIENT_SECRET = config.get("spotify", "client_secret")
REDIRECT_URI: str = "http://localhost:8888/spotify/callback"
SPOTIFY_CLIENT = spotify.Client(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
OAUTH2_SCOPES: Tuple[str] = (
    "user-modify-playback-state",
    "user-read-currently-playing",
    "user-read-playback-state",
    "app-remote-control",
)
OAUTH2: spotify.OAuth2 = spotify.OAuth2(SPOTIFY_CLIENT.id, REDIRECT_URI, scopes=OAUTH2_SCOPES)
TOKEN_FILE = "/tmp/token.dat"


class Item(BaseModel):
    phrase: str


app = FastAPI()


async def token_set(auth_code: str):
    with open(TOKEN_FILE, "wb") as f:
        f.write(auth_code)


async def token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            return f.read().strip()


@app.get("/")
async def main():
    url = None
    if not token():
        url = OAUTH2.url
        return RedirectResponse(url, status_code=302)
    return {"url": url}


@app.post("/play/{track_id}")
async def spotify_play(track_id: str):
    r = httpx.post("https://httpbin.org/post", data={"key": "value"})
    async with httpx.AsyncClient() as client:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = f"grant_type=client_credentials&client_id={SPOTIFY_CLIENT_ID}&client_secret={SPOTIFY_CLIENT_SECRET}"
        response = await client.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        access_token = response.json()["access_token"]

        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {access_token}"}
        data = {"context_uri": f"spotify:album:{track_id}"}
        response = await client.put("https://api.spotify.com/v1/me/player/play", headers=headers, data=data)
        print(response.content)


@app.post("/search/")
async def spotify_search(item: Item):
    async with spotify.Client(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) as client:
        results = await client.search(item.phrase)
        if results.tracks and len(results.tracks) > 0:
            track_url = results.tracks[0].url
            track_id = track_url.split("/")[-1]
    return {"track_url": track_url, "ID": track_id}


@app.get("/spotify/callback")
async def spotify_callback(code: str):
    success = False
    try:
        token_set(code)
    except KeyError:
        return {"ready": False}
    else:
        print(f"Authentiicaton token: {code}")
        async with spotify.Client(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) as client:
            try:
                response = await spotify.User.from_code(client, code, redirect_uri=REDIRECT_URI)
                user = await response
                print(f"Managed to collect user data: {user}")
                return RedirectResponse("/", status_code=302)
            except spotify.errors.HTTPException as e:
                print("Token expired?")
                if "expired" in str(e).lower() or "invalid" in str(e).lower():
                    print("redirect-" * 5)
                    return RedirectResponse("/", status_code=302)
