#!/usr/bin/env python3
from . import db
from . import scraper
from rich.progress import track
from . import *

def load_videos_in_db():
    videos = scraper.get_videos()
    archive = db.ArchiveDB()
    for video in track(videos, description="Adding Video Listings To Database..."):
        if video is not None:
            try:
                archive.add(video)
            except:
                console.stderr("[b]Could not add video:[/b]\t{}".format(video))

def run():
    console.print("Welcome to [b]The Kettle Archive Project[/b]!")
    load_videos_in_db()
    pass


if __name__ == "__main__":
    run()
