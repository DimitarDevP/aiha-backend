from Config.DB.Models import User, AwarenessAlerts
from Config.DB.Schemas import UserSchema, UserForAISchema, AwarenessAlertsSchema


class Tables:
    User = User
    AwarenessAlerts = AwarenessAlerts


class Schemas:
    User = UserSchema()
    Users = UserSchema(many=True)
    UserForAI = UserForAISchema()
    AwarenessAlert = AwarenessAlertsSchema()
    AwarenessAlerts = AwarenessAlertsSchema(many=True)