import configparser
import spotify
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
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
AUTH_TOKEN = None

app = FastAPI()


@app.get("/")
async def main():
    url = None
    if not AUTH_TOKEN:
        url = OAUTH2.url
        return RedirectResponse(url, status_code=302)
    return {"url": url}
