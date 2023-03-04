import yt_dlp
from sys import platform
from . import db
from . import *


def download(video: Video, dir: str, verbose:bool) -> bool:
    outtmpl = str()
    if platform == "win32":
        outtmpl = "{}\\%(title)s [%(id)s].%(ext)s".format(dir)
    else:
        outtmpl = "{}/%(title)s [%(id)s].%(ext)s".format(dir)
    ydl_opts = {
        "format": "bestaudio+bestvideo",
        "encoding": "utf8",
        "merge_output_format": "mp4",
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "postprocessor_args": {
            "ffmpeg": [
                "-c:v",
                "libx265",
                "-filter:v",
                "scale=-1:720,fps=24",
                "-c:a",
                "libfdk_aac",
            ]
        },
        "outtmpl": outtmpl,
        "writethumbnail": True,
        "writedescription": True,
        "verbose": verbose,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(VIDEO_BASE_URL + video.id)
        except:
            console.print_exception(show_locals=True)
            return False
    return True


def download_all(dir: str, verbose:bool) -> bool:
    archive = db.ArchiveDB()
    for vid in archive.get_videos():
        if download(vid, dir, verbose):
            archive.mark_as_saved(vid.id)
