from Config.RouteProvider import RouteProvider
from flask import jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime


class UserCrud(RouteProvider):
    def __init__(self):
        super().__init__()

        self.updatable = [
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

    @jwt_required()
    @RouteProvider.access_controller(["*"])
    def create(self, request):
        # Implemented by Register. No CFF.
        pass

    @jwt_required()
    @RouteProvider.access_controller(["*"])
    def read(self, request):
        params = self.build_params(self.tables.User.__struct__, request.args)
        query_result = self.tables.User.query.filter_by(**params).all()
        return jsonify({"users": self.schemas.Users.dump(query_result), "args": params})

    @jwt_required()
    @RouteProvider.access_controller(["*"])
    def update(self, request):
        data = request.form
        if not self.validate(["id"], data):
            return self._abort(
                400,
                "Incorrect format. Please make sure to send all the required fields.",
            )

        if int(self.auth_user.id) != int(data["id"]):
            return self._abort(403, "You may only edit your user profile.")

        user = self.tables.User.query.filter_by(id=data["id"]).first()
        if user is None:
            return self._abort(404, "User not found.")

        for field in self.updatable:
            if field in data:
                setattr(user, field, data[field])

        self.db.session.commit()

        user = self.schemas.User.dump(user)
        return jsonify({"user": user})

    def delete(self, request):
        data = request.form
        if not self.validate(["id"], data):
            return self._abort(
                400,
                "Incorrect format. Please make sure to send all the required fields.",
            )

        if int(self.auth_user.id) != int(data["id"]):
            return self._abort(403, "You may only edit your user profile.")

        user = self.tables.User.query.filter_by(id=data["id"]).first()
        if user is None:
            return self._abort(404, "User not found.")

        self.db.session.delete(user)
        self.db.session.commit()

        user = self.schemas.User.dump(user)
        return jsonify({"user": user})


user_crud = UserCrud()
