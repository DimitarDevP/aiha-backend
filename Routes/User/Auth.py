from Config.RouteProvider import RouteProvider
from flask import jsonify
from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
import json, datetime


class UserAuth(RouteProvider):
    def __init__(self):
        super().__init__()

    def login(self, request):
        data = request.form
        required_keys = ["email", "password"]

        if not self.validate(required_keys, data):
            return self._abort(
                400, "Incorrect request. Please enter the required fields."
            )

        user = self.tables.User.query.filter_by(
            email=data["email"], password=data["password"]
        ).first()
        if user is None:
            return self._abort(401, "Incorrect email or password.")

        user = self.schemas.User.dump(user)
        _user = json.dumps(user)
        token = create_access_token(_user, expires_delta=datetime.timedelta(days=15))
        refresh = create_refresh_token(_user, expires_delta=datetime.timedelta(days=30))

        return jsonify({"user": user, "access_token": token, "refresh_token": refresh})

    def register(self, request):
        data = request.form
        required_keys = [
            "email",
            "password",
            "date_of_birth",
            "height",
            "weight",
            "illnesses",
            "allergies",
            "addictions",
            "family_history",
            "location_lat",
            "location_lng",
        ]

        constraint = self.check_constraint(data, self.tables.User)
        if constraint is not True:
            return self._abort(409, constraint)

        user = self.tables.User(fullname="")
        [setattr(user, key, data[key]) for key in required_keys]
        self.db.session.add(user)
        self.db.session.commit()

        user = self.tables.User.query.filter_by(email=data["email"]).first()
        token = create_access_token(_user, expires_delta=datetime.timedelta(days=15))
        refresh = create_refresh_token(_user, expires_delta=datetime.timedelta(days=30))

        return jsonify({"user": user, "access_token": token, "refresh_token": refresh})


user_auth = UserAuth()
