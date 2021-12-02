import kvdbms
import models

import pickle
import uuid

_DB_FILE = "/users/guest/t/teikn/Q2PROJ/db.sqlite"


class DBAccess:
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

        key = netid + "." + class_id
        try:
            res = kvdbms.get(key)
            return res
        except:
            return None

    def add_users_role(self, netid, class_id, role):
        """Add a user's role for a course to the database."""

        key = netid + "." + class_id
        try:
            kvdbms.store(key, role)
        except:
            pass

    # TODO - determining key?
    def add_help_instance(self, netid, course_id, question, enqueue_time):
        """Add a help instance to the database."""

        # Create the help id object
        key = uuid.uuid4().hex
        current_instance = models.HelpInstance(key, course_id, netid, question,
                                               enqueue_time)

        # Store in database
        kvdbms.store("HI:" + key, current_instance)

    def claim_help_instance(self, question_id, ta_netid, time):
        """ Update a help instance to indicate a TA is now helping the student"""
        # Get instance out
        current_instance = kvdbms.get("HI:" + question_id)

        # Update
        current_instance.ta_netid = ta_netid
        current_instance.start_help_time = time

        # Reinsert
        kvdbms.store("HI:" + question_id, current_instance)

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
        return models.HelpInstance(*r1)

    def get_active_help_instances(self, course_id):
        """Fetches all HelpInstances that haven't been finished

        Returns an empty list if no HelpInstances waiting"""

        cmd = "SELECT * FROM help_instances WHERE dequeue_time IS NULL AND course_id = :course_id"
        res = list(self.__con.execute(cmd, {"course_id": course_id}))
        waiting = []
        for row in res:
            waiting.append(models.HelpInstance(*row))
        return waiting

    def end_help_instance(self, q_id, end_time):
        """Records the dequeue time for a specific HelpInstance

        Returns the boolean success of the add"""

        cmd = "UPDATE help_instances SET dequeue_time = :dequeue_time WHERE question_id = :id"
        cur = self.__con.cursor()
        cur.execute(cmd, {"dequeue_time": end_time, "id": q_id})
        self.__con.commit()

        return cur.rowcount == 1
