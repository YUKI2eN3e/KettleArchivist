#!/usr/bin/env python3
from . import db
from . import scraper
from rich.progress import track
import argparse
from . import *


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--create-db",
        action="store_true",
        default=False,
        help="Create/Recreate DB",
    )
    parser.add_argument(
        "-u", "--update-db", action="store_true", default=False, help="Update DB"
    )
    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        default=False,
        help="Download Videos (Resume from first non saved entry)",
    )
    parser.add_argument(
        "-r",
        "--redownload",
        action="store_true",
        default=False,
        help="Redownload all videos",
    )
    return parser.parse_args()


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
    args = get_args()
    if args.create_db:
        load_videos_in_db()
    for vid in db.ArchiveDB().get_videos():
        console.print(
            "[b]ID:[/b]\t{}\n[b]Title:[/b]\t{}\n[b]Views:[/b]\t{}\n".format(
                vid.id, vid.title, vid.views
            )
        )
    pass


if __name__ == "__main__":
    run()
