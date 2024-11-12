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


@app.get("/spotify/callback")
async def spotify_callback(code: str):
    return_url = None
    try:
        AUTH_TOKEN = code
    except KeyError:
        return {"ready": False}
    else:
        print(f"Authentiicaton token: {AUTH_TOKEN}")
        async with spotify.Client(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET) as client:
            try:
                response = await spotify.User.from_code(client, code, redirect_uri=REDIRECT_URI)
                user = await response
                results = await client.search("drake")
                print(results.tracks)
                if results.tracks and len(results.tracks) > 0:
                    return_url = results.tracks[0].url
            except spotify.errors.HTTPException as e:
                print("Token expired?")
                if "expired" in str(e).lower() or "invalid" in str(e).lower():
                    print("redirect-" * 5)
                    return RedirectResponse("/", status_code=302)

    return {"url": return_url}
