from rich.console import Console
from rich.traceback import install

install(show_locals=True)

console = Console()

CHANNEL_ID = "@Pikamee"
CHANNEL_URL = "https://www.youtube.com/@Pikamee"
VIDEO_BASE_URL = "https://www.youtube.com/watch?v="
DATABASE_FILE = "KettleArchive.db"

class Video:
	def __init__(self, id:str, title:str, views:int) -> None:
		self.id = id
		self.title = title
		self.views = views