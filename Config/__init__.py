from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flask_marshmallow import Marshmallow
from Config.Common import get_from_env

# Initialization
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = get_from_env("JWT_SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = get_from_env("MYSQL_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Installation
cors = CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)
