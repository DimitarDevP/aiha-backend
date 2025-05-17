from flask import request, Blueprint
from Config.Common import crud_routes

from Routes.User.Crud import user_crud
from Routes.User.Auth import user_auth

users_api = Blueprint("users_api", __name__)


@users_api.route("/crud", methods=["GET", "POST", "PUT", "DELETE"])
def user_crud_routes():
    return crud_routes(request, user_crud)


@users_api.route("/auth/login", methods=["POST"])
def user_login_route():
    return user_auth.login(request)


@users_api.route("/auth/register", methods=["POST"])
def user_register_route():
    return user_auth.register(request)
