import os
from pathlib import Path

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv

# Configuration
parent_dir = Path(__file__).parent.parent
env_path = parent_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Initialization
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

# Installation
cors = CORS(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)
ma = Marshmallow(app)
