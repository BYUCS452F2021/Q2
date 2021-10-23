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
        cmd = ("CREATE TABLE IF NOT EXISTS roles"
               " netid TEXT NOT NULL,"
               " class_id TEXT NOT NULL,"
               " role TEXT NOT NULL")
               #FIXME needs primary key designation for composite key?
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

    def get_users_role(self, netid, class_id):
        """Fetch a user's role for a course from the database.

        Returns None if no such role exists"""

        cmd = "SELECT role FROM roles WHERE netid = :netid AND class_id = :class_id"
        res = self.__con.execute(cmd, {'netid': netid}, {'class_id': class_id})
        r1 = res.fetchone()
        if r1 is None:
            return None
        return r1[0]

    def add_users_role(self, netid, class_id, role):
        """Add a user's role for a course to the database."""

        cmd = ("INSERT INTO roles (netid, class_id, role)"
              " VALUES (:netid, :class_id, :role)")
        res = self.__con.execute(cmd, {'netid': netid}, {'class_id': class_id}, {'role': role})
        self.__con.commit()
