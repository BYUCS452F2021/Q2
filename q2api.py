import flask
from flask import abort, Flask, request, jsonify



import functools
import models
import service

app = Flask(__name__)

class EasyHTTPError(Exception):
    def __init__(self, code, message="HTTP Error"):
        super().__init__(message)
        self.code = code

@app.after_request
def corsify(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET'
    return resp

def require_json(json_args):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            params = request.get_json()
            try:
                return func(*[params[arg] for arg in json_args])
            except KeyError:
                abort(400)
            except EasyHTTPError as httpe:
                abort(httpe.code)
            except Exception as e:
                abort(500)
        return wrapper
    return decorator

@app.route("/user-info", methods=['GET', 'POST'])
@require_json(['netid'])
def get_info(netid):
    name = service.get_users_name(netid)
    return {"name": name}

@app.route("/user-role", methods=['GET', 'POST'])
@require_json(['netid', 'course_id'])
def get_role(netid, course_id):
    role = service.get_usersrole(netid, course_id)
    return {"role": role}

@app.route("/queue-join", methods=['GET', 'POST'])
@require_json(['netid', 'question', 'course_id'])
def queue_join(netid, question, course_id):
    service.join_queue(netid, course_id, question)
    return {"success": True}

@app.route("/claim-question", methods=['GET', 'POST'])
@require_json(['question_id', 'netid', 'course_id'])
def claim_question(q_id, netid, course_id):
    success = service.claim_question(q_id, netid, course_id)
    if not success:
        raise EasyHTTPError(401)
    return {"success": True}

@app.route("/get-waiting-questions", methods=['GET', 'POST'])
@require_json(['netid', 'course_id'])
def get_waiting_questions(netid, course_id):
    qs = service.get_waiting_questions(netid, course_id)
    if qs is None:
        raise EasyHTTPError(401)
    return jsonify(qs)

@app.route("/end-question", methods=['GET', 'POST'])
@require_json(['netid', 'question_id'])
def end_question(netid, q_id):
    success = service.end_question(netid, q_id)
    if not success:
        raise EasyHTTPError(401)
    return {"success": True}