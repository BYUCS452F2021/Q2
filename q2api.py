from flask import Flask

import models
import service

app = Flask(__name__)


@app.route("/q2/user-info/<netid>")
def get_name(netid):
    name = service.get_users_name(netid)
    return f'{{"name"="{name}""}}'

@app.route("/q2/user-role/<netid>/<class_id>")
def get_role(netid, class_id):
    role = service.get_users_role(netid, class_id)
    return {"role: role"}