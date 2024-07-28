import os
import sys
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus

uri_template = os.getenv("STAMPUS_MONGODB_URI")
password = os.getenv("STAMPUS_MONGODB_PASSWORD")

if not uri_template or not password:
    raise ValueError("Environment variables STAMPUS_MONGODB_URI and STAMPUS_MONGODB_PASSWORD must be set")

encoded_password = quote_plus(password)
uri = uri_template.replace("<password>", encoded_password)

client = MongoClient(uri, server_api=ServerApi('1'))
db = client['permits_database']
collection = db['permits']


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def init_db():
    pass

def add_permit(name: str, position: str, valid_until: str, file_path: str) -> str:
    last_permit = collection.find_one(sort=[("permit_number", -1)])
    new_permit_number = str(int(last_permit["permit_number"]) + 1) if last_permit else "1024"
    permit = {
        "name": name,
        "position": position,
        "permit_number": new_permit_number,
        "valid_until": valid_until,
        "file_path": file_path
    }
    collection.insert_one(permit)
    return new_permit_number

def get_permits():
    return list(collection.find())

def delete_permit(permit_id: str):
    try:
        result = collection.delete_one({"_id": ObjectId(permit_id)})
        return result.deleted_count
    except Exception as e:
        print(f"Error deleting permit: {e}")
        return 0

# Initialize the database (if necessary)
init_db()
