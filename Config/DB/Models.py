from Config import db, app
from sqlalchemy.orm import relationship
import datetime


def connect_table_to_key(db, collection_name, foreign_keys, overlaps=None):
    return db.relationship(
        collection_name, foreign_keys=foreign_keys, overlaps=overlaps
    )


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256))
    date_of_birth = db.Column(db.Date)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    illnesses = db.Column(db.String(1024))
    allergies = db.Column(db.String(1024))
    addictions = db.Column(db.String(512))
    family_history = db.Column(db.String(2048))
    location_lat = db.Column(db.Float)
    location_lng = db.Column(db.Float)
    # spouse_id = db.Column(db.Integer, db.ForeignKey('Patient.id'), nullable=True)

    # Spouse = connect_table_to_key(db, 'Patient', foreign_keys=[spouse_id])

    __struct__ = {
        "id": "Number",
        "email": "String",
        "password": "String",
        "date_of_birth": "Number",
        "height": "Number",
        "weight": "Number",
        "illnesses": "String",
        "allergies": "String",
        "addictions": "String",
        "family_history": "String",
        "location_lat": "String",
        "location_lng": "String",
    }
    __unique__ = ["id", "email"]


class AwarenessAlerts(db.Model):
    __tablename__ = "AwarenessAlerts"

    id = db.Column(db.Integer, primary_key=True)
    ai_response = db.Column(db.Text)
    datetime = db.Column(db.DateTime, default=datetime.datetime.now())

    __struct__ = {
        "id": "Number",
        "ai_response": "String",
        "datetime": "String",
    }
    __unique__ = ["id"]
