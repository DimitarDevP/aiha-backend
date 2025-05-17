from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from Config.DB import Schemas, Tables
from Config import db
from flask import jsonify
from functools import wraps
from sqlalchemy.orm import sessionmaker, scoped_session
import random, json


class RouteProvider:
    def __init__(self):
        self.auth_user = None
        self.schemas = Schemas()
        self.tables = Tables()
        self.db = db

    @classmethod
    def access_controller(cls, access_level=["*"]):
        """
        Based on the access_level array, checks if the *authenticated* user request has access to the requested route.
        """

        def decorator(fn):
            @wraps(fn)
            def wrapper(self, *args, **kwargs):
                current_user = get_jwt_identity()
                try:
                    current_user = json.loads(current_user)
                except Exception as e:
                    return cls._abort(418, "I'm a teapot")
                if not current_user:
                    return cls._abort(401, "You are not authorized to access this data")
                tables = Tables()
                user = tables.User.query.filter_by(id=current_user["id"]).first()
                if user is None:
                    return cls._abort(403, "Authentication error. Please log in again")
                # if "*" not in access_level:
                #     schemas = Schemas()
                #     user_schemafied = schemas.User.dump(user)
                #     if user_schemafied["role"]["name"] not in access_level:
                #         return cls._abort(403, "Can't touch this.")
                self.auth_user = user
                return fn(self, *args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def _abort(code, message):
        """
        The function is used to provide an error back to the user with an appropriate code and message (msg).
        """
        return jsonify({"msg": message, "code": code}), code

    def validate(self, keys, data):
        """
        The function validates the request - checks if all the required keys are in the data dictionary
        """
        for key in keys:
            if key not in data:
                return False
        return True

    def check_constraint(self, data, table):
        """
        Checking constraints - making sure that the new entry does not break uniqueness constraints
        """
        for key in table.__unique__:
            if key not in data:
                continue
            res = table.query.filter_by(**{key: data[key]}).first()
            if res is not None and key != "id":
                if "id" in data and int(data["id"]) == res.id:
                    continue
                return (
                    f"Conflict: {key} '{data[key]}' already exists. Use another value."
                )
        return True

    def save_file(self, files, file_key, static_suffix="/", name=None):
        """
        The request object and file key must be passed.
        If static_suffix is not passed, the function assumes static_root as save path.
        If name is not passed, the system will generate one randomly.
        Make sure the root location has been granted 755 privilege and is owned by the same
        user who executes and starts the server
        """
        if name is None:
            name = self.get_random_alphanumerical()

        if file_key not in files:
            return False

        file = files[file_key]
        extension = self.get_extension(file)
        name = name + "." + extension
        file.save("/usr/share/nginx/html/AIHA/" + static_suffix + name)

        return static_suffix + name

    def get_random_alphanumerical(self, _len=16):
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
            alphanumerical += chr(char)
        return alphanumerical

    def get_random_numerical(self, _len=16):
        """
        Provides a truely random numerical string with _len number of characters
        """
        asciiCodes = []
        alphanumerical = ""
        asciiCodes += random.sample(range(48, 57), _len)
        random.shuffle(asciiCodes)
        for char in asciiCodes:
            alphanumerical += chr(char)
        return alphanumerical

    def generate_secret_key(self, length):
        """
        Generates a secret key with length number of characters. The secret key consists of all lower case letters.
        """
        key = ""
        for x in range(length):
            rand = random.randint(97, 122)
            key += chr(rand)
        return key

    def get_extension(self, _f):
        """
        Provides the extension of the _f file
        """
        ext = str(_f.filename.split(".")[len(_f.filename.split(".")) - 1])
        return ext

    def get_hash_info(self, args):
        """
        Extracts the hash information out of the requests and provides info about enabled / key / type
        """
        return {
            "enable_hash": (
                False
                if "enable_hash" not in args or args["enable_hash"] != "true"
                else True
            ),
            "hash_key": "id" if "hash_key" not in args else args["hash_key"],
            "hash_type": (
                True
                if "hash_type" not in args or args["hash_type"] == "cbht"
                else False
            ),
        }

    def build_params(self, keys, args):
        """
        Using the table structure (keys), checks if each key is in the request arguments (args).
        If the key is in args, then it is properly parsed and formatted and returned in the params dictionary
        """
        params = dict()
        for key in keys:
            if key in args:
                if keys[key] == "Integer":
                    params[key] = int(args[key])
                elif keys[key] == "Boolean":
                    params[key] = True if args[key] == "true" else False
                elif args[key] == "null":
                    params[key] = None
                else:
                    params[key] = args[key]
        return params

    def hash_query_results(self, array, col_key, cbht=True):
        """
        Creates a hash table of closed or open bucket type from a specific array with N dictionaries where the key exists inside each dictrionary.
        """
        if type(array) != list:
            array = [array]
        if len(array) == 0:
            return []
        ret = [None for _ in range(max(array, key=lambda x: x[col_key])[col_key] + 1)]

        for item in array:
            if cbht:
                ret[item[col_key]] = item
            else:
                if ret[item[col_key]] is None:
                    ret[item[col_key]] = [item]
                else:
                    ret[item[col_key]].append(item)
        return ret
