import openai, datetime

from Config.Common import get_from_env
from Integrations.Copernicus import get_value_at_location

openai.api_key = get_from_env("OPENAI_API_KEY")


def get_ai_reasoning(user):
    value = get_value_at_location(
    bands=[
        # "CO",
        # "HCHO",
        # "NO2",
        # "O3",
        "SO2", 
        "CH4",
        "AER_AI_340_380", 
        "AER_AI_354_388",
    ],
    date="2025-05-18",
    lon=41.03143,
    lat=21.33474,
)