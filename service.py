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
    dbaccess.DBAccess().add_help_instance(netid, course_id, question,
                                          enqueue_time)


# Check whether a student is a TA for a given class
def verify_is_ta(netid, course_id):

    # Get the role
    user_role = dbaccess.DBAccess().get_users_role(netid, course_id)

    # Check that it is "ta"
    if user_role != "ta":
        return False

    return True


# Claim a question (TA use only)
def claim_question(question_id, netid, course_id):

    # Verify user is a TA
    if verify_is_ta(netid, course_id):
        # Verify question hasn't already been claimed
        current_instance = dbaccess.DBAccess().get_help_instance(question_id)
        if current_instance.ta_netid is None:
            # Get time
            start_help_time = datetime.now()

            # Claim question
            dbaccess.DBAccess().claim_help_instance(question_id, netid,
                                                    start_help_time)
            return True

    return False


def get_active_questions(netid, course_id):
    """Gets all questions that are not yet being helped

    Returns a list of questions with their question text, id, enqueue_time, and the asking student's name
    or None if the requester is not a TA
    """
    if not verify_is_ta(netid, course_id):
        return None

    waiting_instances = dbaccess.DBAccess().get_active_help_instances(
        course_id)

    waiting_questions_return_info = []
    for instance in waiting_instances:
        info = {}
        info["question_id"] = instance.id
        info["student_name"] = get_users_name(instance.student_netid)
        info["question_text"] = instance.question_text
        info["enqueue_time"] = instance.enqueue_time
        info["waiting"] = instance.start_help_time is None
        waiting_questions_return_info.append(info)

    return waiting_questions_return_info


def end_question(netid, q_id):
    """Records that a question has finished being helped

    Returns a boolean success
    """
    help_instance = dbaccess.DBAccess().get_help_instance(q_id)

    # Only the assigned TA can end the question
    if help_instance.ta_netid != netid:
        return False

    curr_time = datetime.now()
    return dbaccess.DBAccess().end_help_instance(q_id, curr_time)
