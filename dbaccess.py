import kvdbms
import models

import pickle
import uuid

_DB_FILE = "/users/guest/t/teikn/Q2PROJ/db.sqlite"


class DBAccess:
    def get_user(self, netid):
        """Fetch a user from the database.

        Returns None if no such user exists"""

        try:
            key = netid
            name = kvdbms.get(key)
            return models.User(name, netid)
        except:
            return None

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

    def add_help_instance(self, netid, course_id, question, enqueue_time):
        """Add a help instance to the database."""

        # Create the help id object
        key = uuid.uuid4().hex
        current_instance = models.HelpInstance(key, course_id, netid, question,
                                               enqueue_time)

        # Add it to active instances
        actives = self.__get_active_help_ids(course_id)
        actives.append(key)

        # Store in database
        kvdbms.store("HI:" + key, current_instance)
        kvdbms.store(course_id + ":active", actives)

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

        Returns None if no such HelpInstance exists"""

        try:
            help_instance = kvdbms.get("HI:" + q_id)
            return help_instance
        except:
            return None

    def __get_active_help_ids(self, course_id):
        """Fetches all HelpInstances IDs that haven't been finished

        Returns an empty list if no HelpInstances waiting"""

        try:
            return kvdbms.get(course_id + ":active")
        except:
            return []

    def get_active_help_instances(self, course_id):
        """Fetches all HelpInstances that haven't been finished

        Returns an empty list if no HelpInstances waiting"""

        active_ids = self.__get_active_help_ids(course_id)

        active_instances = []
        for q_id in active_ids:
            active_instances.append(kvdbms.get("HI:" + q_id))

        return active_instances

    def end_help_instance(self, q_id, end_time):
        """Records the dequeue time for a specific HelpInstance

        Returns the boolean success of the add"""

        try:
            # Fetch stored instance and active instances
            current_instance = kvdbms.get("HI:" + q_id)
            actives = self.__get_active_help_ids(current_instance.course_id)

            # Update
            current_instance.dequeue_time = end_time
            new_actives = [hi for hi in actives if hi != current_instance.id]

            # Store updated instance and active instances
            kvdbms.store("HI:" + q_id, current_instance)
            kvdbms.store(current_instance.course_id + ":active", new_actives)

            return True
        except:
            return False
