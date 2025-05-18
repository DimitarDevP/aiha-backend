import openai, time
from datetime import date

from Config import app
from Config.Common import get_from_env
from Config.DB import Tables, Schemas
from Integrations.Copernicus import get_value_at_location

with app.app_context():
    user = Tables.User.query.filter_by(id=1).first()

def get_aiha_reasoning(user: Tables.User):
    user_info = Schemas.UserForAI.dump(user)
    air_quality = get_value_at_location(
        bands=[
            "CO",
            "HCHO",
            "NO2",
            # "O3",
            # "SO2",
            # "CH4",
            # "AER_AI_340_380",
            # "AER_AI_354_388",
        ],
        date=date.today().isoformat(),
        lon=user.location_lng,
        lat=user.location_lat,
    )
    air_quality["AER_AI_354_388"] = -0.2071281547347704
    air_quality["AER_AI_340_380"] = -0.103115616676708
    air_quality["O3"] = 0.1639051387707392
    content = f"""
        air_quality = {air_quality}
        user_info = {user_info}
    """
    print(content)
    openai.api_key = get_from_env("AIHA_API_KEY")
    thread = openai.beta.threads.create()
    openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=content,
    )

    run = openai.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id="asst_myLzVvaKnGTTG9qU5IXGFnk6",
    )

    while True:
        run_status = openai.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )
        if run_status.status == "completed":
            break
        elif run_status.status in ["failed", "cancelled", "expired"]:
            raise Exception(f"Run failed with status {run_status.status}")
        time.sleep(1)

    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    response = messages.data[0].content[0].text.value
    print(response)

get_aiha_reasoning(user)