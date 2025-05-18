import os
from pathlib import Path
from dotenv import load_dotenv
import sqlalchemy, datetime, random

def str_to_date(str, format="%Y-%m-%d %H:%M:%S"):
    example = datetime.datetime(2021, 6, 2, 9, 39)
    if str == None:
        return False

    if type(str) == type(example):
        return str

    return datetime.datetime.strptime(str, format)


def dict_is_xor(_dict, keys):
    exists = False
    for key in keys:
        if key in _dict and exists == False:
            exists = key
            continue
        if key in _dict and exists != False:
            return False

    return exists


def crud_routes(request, instance):
    method = request.method
    if method == "POST":
        return instance.create(request)
    elif method == "GET":
        return instance.read(request)
    elif method == "PUT":
        return instance.update(request)
    elif method == "DELETE":
        return instance.delete(request)


def get_random_alphanumerical(_len=16):
    """
    Provides a truely random alphanumerical string with _len number of characters
    """
    asciiCodes = []
    alphanumerical = ""
    asciiCodes += random.sample(range(97, 122), int(round(0.375 * _len)))
    asciiCodes += random.sample(range(65, 90), int(round(0.375 * _len)))
    asciiCodes += random.sample(range(48, 57), int(round(0.25 * _len)))
    random.shuffle(asciiCodes)
    for char in asciiCodes:
        alphanumerical += str(char)
    return int(alphanumerical)


def get_from_env(variable_name):
    parent_dir = Path(__file__).parent.parent
    env_path = parent_dir / ".env"
    load_dotenv(dotenv_path=env_path)
    return os.getenv(variable_name)