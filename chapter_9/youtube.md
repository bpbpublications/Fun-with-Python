# test

```bash
curl https://www.googleapis.com/youtube/v3/search\?part\=snippet\&type\=channel\&fields\=items%2Fsnippet%2FchannelId\&q\=CafeDeAnatolia\&key\=<your API key>
```

output

```json
{
  "items": [
    {
      "snippet": {
        "channelId": "UC1Tr6S-XLBk1NzNX1jErWMg"
      }
    },
    {
      "snippet": {
        "channelId": "UCrJ9Cdr93XCbU_waM0gbBqQ"
      }
    },
    {
      "snippet": {
        "channelId": "UCehwgzlM3jtgWJjkIUgyITw"
      }
    },
    {
      "snippet": {
        "channelId": "UCbeBZM7pkb8UmzAz-Sy39og"
      }
    },
    {
      "snippet": {
        "channelId": "UCnKq9RD9agkJ6Aztw9Sl_yg"
      }
    }
  ]
}
```

# API key


## missing API key

```python
>>> import asyncio
>>> from youtube_api import YouTube
>>> yt = YouTube('some channel name')
>>> asyncio.run(yt.get_channel_id())

File ~/work/fun-with-python/chapter_9/youtube_api.py:17, in YouTube.api_key(self)
     14 @property
     15 def api_key(self):
     16     if not getattr(self, '_api_key', None):
---> 17         raise Exception("Please specify API key before making calls")
     18     return self._api_key

Exception: Please specify API key before making calls
```

## specify empty API key

```python
>>> from youtube_api import YouTube
>>> yt = YouTube('some channel name')
>>> yt.api_key = ""
\---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
Cell In[10], line 1
----> 1 yt.api_key = None

File ~/work/fun-with-python/chapter_9/youtube_api.py:23, in YouTube.api_key(self, value)
     20 @api_key.setter
     21 def api_key(self, value):
     22     if not value:
---> 23         raise Exception("Please specify valid API key")
     24     self._api_key = value

Exception: Please specify valid API key
```

## valid call

```bash
$ python youtube_api.py --channel CafeDeAnatolia --api-key <your api key>

Calling https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&fields=items%2Fsnippet%2FchannelId&q=CafeDeAnatolia&key=<your api key>
got channel ID: UC1Tr6S-XLBk1NzNX1jErWMg
```


# video URL

```sh
curl -X POST -H "Content-Type: application/json" -d '{"context": {"client": {"clientName": "WEB", "clientVersion": "2.20231026.03.01"}}, "videoId": "zSd9kCvYcOg"}' \
https://www.youtube.com/youtubei/v1/player\?key\=<your api key>\&prettyPrint\=false | jq
```

response

```
{
  ...
  "streamingData": {
    "expiresInSeconds": "21540",
    "formats": [
      {
        "itag": 18,
        "url": "https://rr2---sn-5hneknes.googlevideo.com/(...)",
        "mimeType": "video/mp4; codecs=\"avc1.42001E, mp4a.40.2\"",
        "bitrate": 656697,
        "width": 640,
        "height": 360,
        "lastModified": "1698589609182367",
        "contentLength": "137118494",
        "quality": "medium",
        "fps": 25,
        "qualityLabel": "360p",
        "projectionType": "RECTANGULAR",
        "averageBitrate": 656671,
        "audioQuality": "AUDIO_QUALITY_LOW",
        "approxDurationMs": "1670466",
        "audioSampleRate": "44100",
        "audioChannels": 2
      },
      {
        "itag": 22,
        "url": "https://rr2---sn-5hneknes.googlevideo.com/(...)",
        "mimeType": "video/mp4; codecs=\"avc1.64001F, mp4a.40.2\"",
        "bitrate": 1104970,
        "width": 1280,
        "height": 720,
        "lastModified": "1698592104844652",
        "quality": "hd720",
        "fps": 25,
        "qualityLabel": "720p",
        "projectionType": "RECTANGULAR",
        "audioQuality": "AUDIO_QUALITY_MEDIUM",
        "approxDurationMs": "1670466",
        "audioSampleRate": "44100",
        "audioChannels": 2
      }
    ],
  }
}
```
