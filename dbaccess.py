import sqlite3
import models

_DB_FILE = "/users/guest/t/teikn/Q2PROJ/db.sqlite"


class DBAccess:
    __con = sqlite3.connect(_DB_FILE)

    def __init__(self) -> None:
        self.__con = sqlite3.connect(_DB_FILE)

    def init_db(self):
        cmd = ("CREATE TABLE IF NOT EXISTS"
               " users (netid TEXT NOT NULL PRIMARY KEY, name TEXT NOT NULL)")
        self.__con.execute(cmd)
        self.__con.commit()

    def get_user(self, netid):
        """Fetch a user from the database.

        Returns None if no such user exists,
        or if two users with that netid exits (should never happen)"""

        cmd = "SELECT name FROM users WHERE netid = :netid"
        res = self.__con.execute(cmd, {'netid': netid})
        r1 = res.fetchone()
        if r1 is None:
            return None
        else:
            if res.fetchone() is not None:
                return None
        return models.User(r1[0], netid)
