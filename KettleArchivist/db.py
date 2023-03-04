import sqlite3
from typing import List
from . import *


class ArchiveDB:
    def __init__(self, file: str = None) -> None:
        if file is None:
            self.db = sqlite3.connect(DATABASE_FILE)
        else:
            self.db = sqlite3.connect(file)
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS VIDEOS (
            ID		TEXT 	PRIMARY KEY 	NOT NULL,
            TITLE	TEXT	NOT NULL,
            VIEWS   INT     NOT NULL,
            SAVED	BOOL	NOT NULL
            );"""
        )
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS SHORTS (
            ID		TEXT 	PRIMARY KEY 	NOT NULL,
            TITLE	TEXT	NOT NULL,
            SAVED	BOOL	NOT NULL
            );"""
        )

    def add(self, video: Video) -> bool:
        if video.views >= 0:
            return self.add_video(video.id, video.title, video.views)
        else:
            return self.add_short(video.id, video.title)

    def add_video(
        self, id: str, title: str = None, views: int = 0, saved=False
    ) -> bool:
        """
        Parameters
        ----------
        id : str
                the video id (e.g. for "https://www.youtube.com/watch?v=MJ4f7bpNnis" the id is "MJ4f7bpNnis")
        title : str
                the title of the video
        views : int
                the number of views the video has
        saved : bool
                wether the video has been saved or not

        Returns
        -------
        bool
                return true if sucessful
        """
        try:
            self.db.execute(
                "INSERT INTO VIDEOS (ID, TITLE, VIEWS, SAVED) VALUES(?, ?, ?, ?)",
                (id, title, views, saved),
            )
            self.db.commit()
        except Exception:
            console.print_exception(show_locals=True)
            return False
        return True

    def add_short(self, id: str, title: str = None, saved=False) -> bool:
        """
        Parameters
        ----------
        id : str
                the short id (e.g. for "https://www.youtube.com/watch?v=MJ4f7bpNnis" the id is "MJ4f7bpNnis")
        title : str
                the title of the short
        saved : bool
                wether the short has been saved or not

        Returns
        -------
        bool
                return true if sucessful
        """
        try:
            self.db.execute(
                "INSERT INTO SHORTS (ID, TITLE, SAVED) VALUES(?, ?, ?)",
                (id, title, saved),
            )
            self.db.commit()
        except Exception:
            console.print_exception(show_locals=True)
            return False
        return True

    def mark_as_saved(self, id: str) -> bool:
        """
        Parameters
        ----------
        id : str
                the id of the video that has been saved

        Returns
        -------
        bool
                return true if sucessful
        """
        try:
            self.db.execute("UPDATE VIDEOS set SAVED = TRUE where ID = ?", (id,))
            self.db.commit()
        except Exception:
            console.print_exception(show_locals=True)
            return False
        return True

    def get_videos(self) -> List[Video]:
        videos = list()
        try:
            cur = self.db.cursor()
            cur.execute("SELECT * FROM VIDEOS where SAVED = FALSE ORDER BY VIEWS DESC")
            rows = cur.fetchall()
            for row in rows:
                videos.append(Video(row[0], row[1], row[2]))
        except Exception:
            console.print_exception(show_locals=True)
            return False
        return videos
