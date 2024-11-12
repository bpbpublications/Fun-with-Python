import asyncio
import click
import httpx
import urllib


class YouTube:

    base_url = "https://www.googleapis.com/youtube/v3/"

    def __init__(self, channel):
        self.channel_name = channel

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


@click.command()
@click.option("--channel", help="Channel name to scan")
@click.option("--api-key", default=None, help="YouTube API key")
def main(api_key, channel):
    yt = YouTube(channel)
    yt.api_key = api_key
    run_app = yt.get_videos_list()
    asyncio.run(run_app)


if __name__ == "__main__":
    main()
