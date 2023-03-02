import sqlite3
from . import *


class ArchiveDB:
    def __init__(self, file: str = None) -> None:
        self.db = sqlite3.connect("KettleArchive.db")
        if file is None:
            self.db.execute(
                """CREATE TABLE VIDEOS (
				ID		TEXT 	PRIMARY KEY 	NOT NULL,
				TITLE	TEXT	NOT NULL,
				SAVED	BOOL	NOT NULL
			);"""
            )

    def add_video(self, id: str, title: str = None, saved=False) -> bool:
        """
        Parameters
        ----------
        id : str
                the video id (e.g. for "https://www.youtube.com/watch?v=MJ4f7bpNnis" the id is "MJ4f7bpNnis")
        title : str
                the title of the video
        saved : bool
                wether the video has been saved or not

        Returns
        -------
        bool
                return true if sucessful
        """
        try:
            self.db.execute(
                "INSERT INTO VIDEOS (ID, TITLE, SAVED) VALUES(?, ?, ?)",
                [id, title, saved],
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
            self.db.execute("UPDATE VIDEOS set SAVED = TRUE where ID = ?", id)
            self.db.commit()
        except Exception:
            console.print_exception(show_locals=True)
            return False
        return True
