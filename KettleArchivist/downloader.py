import yt_dlp
from yt_dlp.postprocessor import (
    ExecPP,
    FFmpegThumbnailsConvertorPP,
    MetadataFromFieldPP,
    MetadataParserPP,
    FFmpegVideoConvertorPP,
    FFmpegPostProcessor,
)
from . import db
from . import *


def download(video: Video) -> bool:
    ydl_opts = {
        "format": "bestaudio/best",
        "encoding": "utf8",
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "postprocessor_args": {
            "videoconverter": [
                "-c:v",
                "libx265",
                "-filter:v",
                "scale=-1:720,fps=24",
                "-c:a",
                "libfdk_aac",
            ]
        },
        "merge_output_format": "mp4",
        "outtmpl": "%(title)s [%(id)s].%(ext)s",
        "write_thumbnail": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download(VIDEO_BASE_URL + video.id)
        except:
            console.print_exception(show_locals=True)
            return False
    return True


def download_all() -> bool:
    archive = db.ArchiveDB()
    for vid in archive.get_videos():
        if download(vid):
            archive.mark_as_saved(vid.id)
