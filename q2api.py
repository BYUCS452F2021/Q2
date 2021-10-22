from flask import Flask

import models
import service

app = Flask(__name__)


@app.route("/q2/user-info/<netid>")
def get_name(netid):
    name = service.get_users_name(netid)
    return f'{{"name"="{name}""}}'
