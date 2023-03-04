import yt_dlp
from typing import List
from rich.progress import track
import json
from . import *

def get_videos(opts:dict={}) -> List[Video]:
    opts['ignoreerrors'] = True
    videos = list()
    with yt_dlp.YoutubeDL(opts) as ydl:
        vids = ydl.extract_info(CHANNEL_URL, download=False)['entries']
        with open('datadump.json', 'w', encoding='utf8') as datadump:
            datadump.writelines(vids)
        for vid in track(vids, description="Collecting Video Info From Channel..."):
            try:
                videos.append(Video(vid['id'], vid['title'], vid['view_count']))
            except:
                console.stderr("[b]Keys:[/b]\t{}\n[b]Info:[/b]\t{}\n".format(
                    vid.keys(), vid
                ))
                try:
                    videos.append(Video(vid['id'], vid['title'], -1))
                except:
                    continue
    return videos