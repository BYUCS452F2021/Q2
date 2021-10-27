import sqlite3
import models

_DB_FILE = "/users/guest/t/teikn/Q2PROJ/db.sqlite"


class DBAccess:
    __con = sqlite3.connect(_DB_FILE)

    def __init__(self) -> None:
        self.__con = sqlite3.connect(_DB_FILE)

    def init_db(self):
        cmd = ("CREATE TABLE IF NOT EXISTS users("
               " netid TEXT NOT NULL PRIMARY KEY,"
               " name TEXT NOT NULL)")
        self.__con.execute(cmd)
        self.__con.commit()
        cmd = ("CREATE TABLE IF NOT EXISTS help_instances("
               " id TEXT NOT NULL PRIMARY KEY,"
               " course_id TEXT NOT NULL,"
               " student_netid TEXT NOT NULL,"
               " question_text TEXT NOT NULL,"
               " enqueue_time TIMESTAMP NOT NULL,"
               " dequeue_time TIMESTAMP,"
               " start_help_time TIMESTAMP,"
               " ta_netid TEXT)")
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

    def get_help_instance(self, id):
        """Fetches a HelpInstance from the database

        Returns None if no such HelpInstance exists
        or if two HelpInstances with the same internal id exist"""

        cmd = "SELECT * FROM help_instances WHERE id = :id"
        res = self.__con.execute(cmd, {"id": id})
        r1 = res.fetchone()
        if r1 is None:
            return None
        else:
            if res.fetchone() is not None:
                return None
        return models.HelpInstance(r1[0], r1[1], r1[2], r1[3], r1[4], r1[5], r1[6], r1[7])

    def get_waiting_help_instances(self, course_id):
        """Fetches all HelpInstances that haven't started being helped

        Returns an empty list if no HelpInstances waiting"""

        cmd = "SELECT * FROM help_instances WHERE ta_netid IS NULL AND course_id = :course_id"
        res = list(self.__con.execute(cmd, {"course_id": course_id}))
        waiting = []
        for row in res:
            waiting.append(models.HelpInstance(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
        return waiting

    def end_help_instance(self, id, end_time):
        """Records the dequeue time for a specific HelpInstance

        Returns the boolean success of the add"""

        cmd = "UPDATE help_instances SET dequeue_time = :dequeue_time WHERE id = :id"
        cur = self.__con.cursor()
        cur.execute(cmd, {"dequeue_time": end_time, "id": id})
        self.__con.commit()

        return cur.rowcount == 1
