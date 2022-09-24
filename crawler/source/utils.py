import json
import os
from datetime import datetime as dt


def pre_tag_to_json(html_source):
    return json.loads(html_source.find("pre").text)


def json_dump(obj):
    print(json.dumps(obj, indent=2))


def create_file(name):
    now = dt.now()
    format_timestamp = now.strftime("%Y%m%d%H%M%S")

    dir_path = os.path.join(os.getcwd(), "output", "temp")

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_name = f"{format_timestamp}-{name}"
    file_path = os.path.join(dir_path, file_name)

    return file_path


def create_json_file(file_name, data):
    with open(create_file(file_name), "w") as file:
        jsonString = json.dumps(data)
        file.write(jsonString)


def get_last_page(obj):
    return obj["paging"]["last_page"]
