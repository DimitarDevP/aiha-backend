from Config import app, db
from Config.RouteProvider import RouteProvider
from flask_requests import request
from flask import jsonify

from Routes.User import users_api

app.register_blueprint(users_api, url_prefix="/users/")


@app.route("/meta", methods=["GET"])
def meta():
    return jsonify({"version": "0.0.1"})


if __name__ == "__main__":
    app.run()
