import yt_dlp
from typing import List
from rich.progress import track
import json
from . import *

def get_videos(opts:dict={}) -> List[Video]:
    opts['ignoreerrors'] = True
    opts['format'] = 'bestaudio/best'
    videos = list()
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(CHANNEL_URL, download=False)
        vids = info['entries'][0]['entries']
        lives = info['entries'][1]['entries']
        shorts = info['entries'][2]['entries']
        with open('datadump.json', 'w', encoding='utf8') as datadump:
            datadump.writelines(json.dumps(vids))
        if vids is not None:
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
        if lives is not None:
            for live in track(lives, description="Collecting Live Info From Channel..."):
                try:
                    videos.append(Video(live['id'], live['title'], live['view_count']))
                except:
                    console.stderr("[b]Keys:[/b]\t{}\n[b]Info:[/b]\t{}\n".format(
                        live.keys(), live
                    ))
                    try:
                        videos.append(Video(live['id'], live['title'], -1))
                    except:
                        continue
        if shorts is not None:
            for short in track(shorts, description="Collecting Short Info From Channel..."):
                try:
                    videos.append(Video(short['id'], short['title'], -1))
                except:
                    console.stderr("[b]Keys:[/b]\t{}\n[b]Info:[/b]\t{}\n".format(
                        short.keys(), short
                    ))
                    continue
    return videos