import configparser
import httpx
import os
import spotify
import webbrowser
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
    play_url = f"https://open.spotify.com/track/{track_id}"
    webbrowser.open(play_url)


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