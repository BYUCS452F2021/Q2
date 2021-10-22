"""
Questions:
- Should there be a role variable? Roles can vary between courses
- Not private classes so no getters/setters?
- Any other functionality?
"""


class User:
    """ A human at BYU that has some involvement with CS classes """
    def __init__(self, name, netid):
        self.name = name
        self.netid = netid


class HelpInstance:
    """ A representation of when a student gets in line on the queue. """
    def __init__(self, course_id, student_netid, question_text, enqueue_time,
                 dequeue_time, start_help_time, ta_netid):
        self.course_id = course_id
        self.student_netid = student_netid
        self.question_text = question_text
        self.enqueue_time = enqueue_time
        self.dequeue_time = dequeue_time
        self.start_help_time = start_help_time
        self.ta_netid = ta_netid


class Course:
    """ A CS course """
    def __init__(self, course_id, course_name, queue_open):
        self.couse_id = course_id
        self.course_name = course_name
        self.queue_open = queue_open
