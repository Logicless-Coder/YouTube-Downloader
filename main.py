#!/usr/bin/youtube-downloader/env python3

import sys
from pytube import YouTube, Playlist
from pathlib import Path


def download_video(url, audio, output):
    yt = YouTube(url)
    if audio:
        stream = yt.streams.filter(only_audio=True).get_audio_only()
    else:
        stream = yt.streams.filter(progressive=True).get_highest_resolution()
    print(f"Downloading {stream.title} to {output}")
    stream.download(output)


def download_playlist(url, audio, output):
    pl = Playlist(url)
    output = output.joinpath(pl.title)
    print(f"Downloading playlist {pl.title} [{pl.length}]")
    for video in pl.videos:
        download_video(video.watch_url, audio, output)


usage = 'Usage: python main.py <url> <a/v> <playlist?> <output?>'
url = ""
output = Path.cwd()
print(output)
audio = False
playlist = False


if len(sys.argv) < 2:
    print(usage)
    sys.exit(1)
if len(sys.argv) >= 2:
    url = sys.argv[1]
if len(sys.argv) >= 3:
    if sys.argv[2] == "a":
        audio = True
        output = output.joinpath('Music')
    else:
        output = output.joinpath('Videos')
if len(sys.argv) >= 4:
    if sys.argv[3] == "p":
        playlist = True
# if len(sys.argv) >= 5:
#     print(sys.argv[4])
#     output = Path.cwd().joinpath(str(sys.argv[4])).mkdir(
#         parents=True, exist_ok=True)

try:
    if playlist:
        download_playlist(url, audio, output)
    else:
        download_video(url, audio, output)
except Exception as e:
    print("Some error occured.", e)
    sys.exit(1)
