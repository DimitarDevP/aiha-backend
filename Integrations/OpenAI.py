import openai, time
from datetime import date

from Config import app
from Config.Common import get_from_env
from Config.DB import Tables, Schemas
from Integrations.Copernicus import get_value_at_location

with app.app_context():
    user = Tables.User.query.filter_by(id=1).first()


def get_chat_history(thread_id: str):
    return openai.beta.threads.messages.list(thread_id=thread_id).data


def get_aiha_reasoning(user: Tables.User, thread_id=None, message=None):
    openai.api_key = get_from_env("AIHA_API_KEY")
    if thread_id is None:
        user_info = Schemas.UserForAI.dump(user)
        air_quality = get_value_at_location(
            bands=[
                "CO",
                "HCHO",
                "NO2",
                "O3",
                "SO2",
                "CH4",
                "AER_AI_340_380",
                "AER_AI_354_388",
            ],
            date=date.today().isoformat(),
            lon=user.location_lat,
            lat=user.location_lng,
        )
        print(air_quality)
        content = f"""
            air_quality = {air_quality}
            user_info = {user_info}
        """
        thread = openai.beta.threads.create()
        thread_id = thread.id
    else:
        thread = openai.beta.threads.retrieve(thread_id)
        content = message

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
    return {
        "is_first_message": True if message is None else False,
        "message": response[7 : len(response) - 3] if message is None else response,
        "thread_id": thread_id,
    }

if __name__ == "__main__":
    get_aiha_reasoning(user)