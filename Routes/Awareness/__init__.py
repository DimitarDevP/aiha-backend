from flask import request, Blueprint
from Config.Common import crud_routes
from Config.RouteProvider import RouteProvider
from flask import jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

awareness_api = Blueprint("awareness_api", __name__)

class AwarenessCrud(RouteProvider):
    def __init__(self):
        super().__init__()

    @jwt_required()
    @RouteProvider.access_controller(["*"])
    def read(self, request):
        user = self.auth_user
        # TIME IS CRUSHING US DO NOT JUDGE THIS CODE
        return jsonify({
            "awareness": self.schemas.AwarenessAlerts.dump(self.tables.AwarenessAlerts.query.all())
        })

awareness_crud = AwarenessCrud()

@awareness_api.route("/crud", methods=["GET"])
def awareness_crud_routes():
    return crud_routes(request, awareness_crud)