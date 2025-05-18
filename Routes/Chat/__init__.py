from flask import request, Blueprint
from Config.Common import crud_routes
from Config.RouteProvider import RouteProvider
from Integrations.OpenAI import get_aiha_reasoning
from flask import jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime

chat_api = Blueprint("chat_api", __name__)

class Chat(RouteProvider):
    def __init__(self):
        super().__init__()


    @jwt_required()
    @RouteProvider.access_controller(["*"])
    def send_message(self, request):
        data = request.form
        
        if "message" in data and "thread_id" in data:
            return get_aiha_reasoning(self.auth_user, data["thread_id"], data["message"])
        else:
            return get_aiha_reasoning(self.auth_user)

chat = Chat()

@chat_api.route("/send_message", methods=["POST"])
def send_message_route():
    return chat.send_message(request)