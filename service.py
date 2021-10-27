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

def get_waiting_questions(netid, course_id):
  """Gets all questions that are not yet being helped

  Returns a list of quesitons with their question text, id, enqueue_time, and the asking student's name
  or None if the requester is not a TA
  """
  if not verify_is_ta(netid, course_id):
    return None
  
  waiting_instances = dbaccess.DBAccess().get_waiting_help_instances(course_id)
  
  waiting_questions_return_info = []
  for instance in waiting_instances:
    info = {}
    info["question_id"] = instance.id
    info["student_name"] = get_users_name(instance.student_netid)
    info["question_text"] = instance.question_text
    info["enqueue_time"] = instance.enqueue_time
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