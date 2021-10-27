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
               " question_id INTEGER NOT NULL PRIMARY KEY,"
               " course_id TEXT NOT NULL,"
               " student_netid TEXT NOT NULL,"
               " question TEXT NOT NULL,"
               " enqueue_time TIMESTAMP NOT NULL,"
               " dequeue_time TIMESTAMP,"
               " start_help_time TIMESTAMP,"
               " ta_netid TEXT)")
        self.__con.execute(cmd)
        self.__con.commit()

        cmd = ("CREATE TABLE IF NOT EXISTS roles ("
               " netid TEXT NOT NULL,"
               " class_id TEXT NOT NULL,"
               " role TEXT NOT NULL,"
               " PRIMARY KEY (netid, class_id) )")
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
        res = self.__con.execute(cmd, {'netid': netid, 'class_id': class_id})
        r1 = res.fetchone()
        if r1 is None:
            return None
        return r1[0]

    def add_users_role(self, netid, class_id, role):
        """Add a user's role for a course to the database."""

        cmd = ("INSERT INTO roles (netid, class_id, role)"
               " VALUES (:netid, :class_id, :role)")
        res = self.__con.execute(cmd, {
            'netid': netid,
            'class_id': class_id,
            'role': role
        })
        self.__con.commit()

    def add_help_instance(self, netid, course_id, question, enqueue_time):
        """Add a help instance to the database."""
        cmd = (
            "INSERT INTO help_instances (student_netid, course_id, question, enqueue_time)"
            " VALUES (:student_netid, :course_id, :question, :enqueue_time)")
        res = self.__con.execute(
            cmd, {
                'student_netid': netid,
                'course_id': course_id,
                'question': question,
                'enqueue_time': enqueue_time
            })
        self.__con.commit()

    def claim_help_instance(self, question_id, ta_netid, time):
        """ Update a help instance to indicate a TA is now helping the student"""
        cmd = ("UPDATE help_instances"
               " SET ta_netid = :ta_netid, start_help_time = :time"
               " WHERE question_id = :question_id")
        res = self.__con.execute(cmd, {
            'ta_netid': ta_netid,
            'question_id': question_id,
            'time': time
        })
        self.__con.commit()

    def get_help_instance(self, q_id):
        """Fetches a HelpInstance from the database

        Returns None if no such HelpInstance exists
        or if two HelpInstances with the same internal id exist"""

        cmd = "SELECT * FROM help_instances WHERE question_id = :id"
        res = self.__con.execute(cmd, {"id": q_id})
        r1 = res.fetchone()
        if r1 is None:
            return None
        else:
            if res.fetchone() is not None:
                return None
        return models.HelpInstance(r1[0], r1[1], r1[2], r1[3], r1[4], r1[5],
                                   r1[6], r1[7])

    def get_waiting_help_instances(self, course_id):
        """Fetches all HelpInstances that haven't started being helped

        Returns an empty list if no HelpInstances waiting"""

        cmd = "SELECT * FROM help_instances WHERE ta_netid IS NULL AND course_id = :course_id"
        res = list(self.__con.execute(cmd, {"course_id": course_id}))
        waiting = []
        for row in res:
            waiting.append(
                models.HelpInstance(row[0], row[1], row[2], row[3], row[4],
                                    row[5], row[6], row[7]))
        return waiting

    def end_help_instance(self, q_id, end_time):
        """Records the dequeue time for a specific HelpInstance

        Returns the boolean success of the add"""

        cmd = "UPDATE help_instances SET dequeue_time = :dequeue_time WHERE question_id = :id"
        cur = self.__con.cursor()
        cur.execute(cmd, {"dequeue_time": end_time, "id": q_id})
        self.__con.commit()

        return cur.rowcount == 1
