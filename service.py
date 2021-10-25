"""
Questions:
- Will DBAccess be implemented as classes or just functions?
- Are we using snake_case or camelCase for functions?
- How do we want to handle missing data? Where do we want to handle it?
"""
from sqlite3.dbapi2 import DatabaseError
import dbaccess
from datetime import datetime


# Get a user's name from their netID
def get_users_name(netid):
    user = dbaccess.DBAccess().get_user(netid)
    if user is None:
        name = "Student"
    else:
        name = user.name

    return name

def get_usersrole(netid, class_id):
    role = dbaccess.DBAccess().get_users_role(netid, class_id)
    if role is None:
        dbaccess.DBAccess().add_users_role(netid, class_id, "student")
        return "student"

    return role
# Add a help instance to the correct queue
def join_queue(netid, course_id, question):

    # Get enqueue time
    enqueue_time = datetime.now()

    # Add to database
    dbaccess.DBAccess().add_help_instance(course_id, question, enqueue_time)


# Check whether a student is a TA for a given class
def verify_is_ta(netid, course_id):

    # Get the role
    user_role = dbaccess.DBAccess.get_users_role(netid, course_id)

    # Check that it is "TA"
    if user_role is not "TA":
        return False

    return True

# Claim a question (TA use only)
def claim_question(question_id, netid, course_id):

    # Verify user is a TA
    if verify_is_ta(netid, course_id):
        # Verify question hasn't already been claimed
        current_instance = dbaccess.DBAccess.get_help_instance(question_id)
        if current_instance.ta_netid is None:
            # Get time
            start_help_time = datetime.now()

            # Claim question
            dbaccess.DBAccess.claim_help_instance(question_id, netid, start_help_time)
            return True

    return False
