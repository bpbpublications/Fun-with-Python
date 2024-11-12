import asyncio
import click
import httpx
import tempfile
import urllib
from download_pool_and_chunks import Downloader
from typing import List


class YouTube:

    base_url = "https://www.googleapis.com/youtube/v3/"

    def __init__(self, channel):
        self.channel_name = channel
        self._downloader = Downloader()
        self.video_quality = "720p"

    @property
    def api_key(self):
        if not getattr(self, "_api_key", None):
            raise Exception("Please specify API key before making calls")
        return self._api_key

    @property
    async def channel_id(self):
        if not getattr(self, "_channel_id", None):
            self._channel_id = await self.get_channel_id()
        return self._channel_id

    @api_key.setter
    def api_key(self, value):
        if not value:
            raise Exception("Please specify valid API key")
        self._api_key = value

    def _encode_query(self, query):
        return urllib.parse.urlencode(query)

    async def get_channel_id(self):
        query = {
            "part": "snippet",
            "type": "channel",
            "fields": "items/snippet/channelId",
            "q": self.channel_name,
            "key": self.api_key,
        }
        url = f"{self.base_url}search?{self._encode_query(query)}"
        click.echo(f"Calling {url}")
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            if response.status_code == 200:
                response_data = response.json()
                channel_id = response_data["items"][0]["snippet"]["channelId"]
                click.echo(f"got channel ID: {channel_id}")
                return channel_id

    async def get_videos_list(self):
        query = {
            "key": self.api_key,
            "channelId": await self.channel_id,
            "part": "snippet,id",
            "order": "date",
            "maxResults": 20,
        }
        videos = []
        url = f"{self.base_url}search?{self._encode_query(query)}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True)
            if response.status_code == 200:
                response_data = response.json()
                videos = [{v["id"]["videoId"]: v["snippet"]["title"]} for v in response_data["items"]]
        return videos

    async def get_video_download_link(self, video_id):
        query = {"key": self.api_key, "prettyPrint": False}
        url = "https://www.youtube.com/youtubei/v1/player"
        url = f"{url}?{self._encode_query(query)}"
        data = {
            "context": {
                "client": {
                    "clientName": "WEB",
                    "clientVersion": "2.20231026.03.01",
                    "clientScreen": "WATCH",
                    "mainAppWebInfo": {"graftUrl": f"/watch?v={video_id}"},
                },
                "user": {"lockedSafetyMode": False},
                "request": {"useSsl": True, "internalExperimentFlags": [], "consistencyTokenJars": []},
            },
            "videoId": video_id,
            "racyCheckOk": False,
            "contentCheckOk": False,
        }
        click.echo(f"Fetchnig video details: {video_id}")
        headers = {"user-agent": "Mozilla/5.0 (platform; rv:geckoversion) Gecko/geckotrail Firefox/firefoxversion"}
        from pprint import pprint

        async with httpx.AsyncClient() as client:
            result = await client.post(url, json=data)
            # pprint(result.json())
            for item in result.json().get("streamingData", {}).get("formats", []):
                print(item.get("qualityLabel"))
                if item.get("qualityLabel") == self.video_quality:
                    return item.get("url")

    async def download_videos(self, videos_list: List[str]):
        # to make it compatible with Downloader we have to send list to file
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"\n".join(videos_list))
            click.echo(f"Start downloading {len(videos_list)} elements")
            await self._downloader.download_list(f.name)

    async def download_channel_videos(self):
        videos = await self.get_videos_list()
        links_to_download = []
        for item in videos:
            video_id, title = list(item.items())[0]
            video_link = await self.get_video_download_link(video_id)
            click.echo(f"Got downloadable link {title} ({video_id}): {video_link}")
            if video_link:
                links_to_download.append(video_link.encode())
        await self.download_videos(links_to_download)


@click.command()
@click.option("--channel", help="Channel name to scan")
@click.option("--api-key", default=None, help="YouTube API key")
def main(api_key, channel):
    yt = YouTube(channel)
    yt.api_key = api_key
    run_app = yt.download_channel_videos()
    asyncio.run(run_app)


if __name__ == "__main__":
    main()
