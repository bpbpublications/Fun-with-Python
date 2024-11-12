import subprocess
import miniaudio

channels = 2
sample_rate = 44100
sample_width = 2  # 16 bit pcm
filename = "samples/music.m4a"  # AAC encoded audio file


def stream_pcm(source):
    required_frames = yield b""  # generator initialization
    while True:
        required_bytes = required_frames * channels * sample_width
        sample_data = source.read(required_bytes)
        if not sample_data:
            break
        print(".", end="", flush=True)
        required_frames = yield sample_data


with miniaudio.PlaybackDevice(
    output_format=miniaudio.SampleFormat.SIGNED16, nchannels=channels, sample_rate=sample_rate
) as device:
    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-v",
            "fatal",
            "-hide_banner",
            "-nostdin",
            "-i",
            filename,
            "-f",
            "s16le",
            "-acodec",
            "pcm_s16le",
            "-ac",
            str(channels),
            "-ar",
            str(sample_rate),
            "-",
        ],
        stdin=None,
        stdout=subprocess.PIPE,
    )
    stream = stream_pcm(ffmpeg.stdout)
    next(stream)  # start the generator
    device.start(stream)
    input("Audio file playing in the background. Enter to stop playback: ")
    ffmpeg.terminate()
