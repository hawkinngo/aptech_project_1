import json
import os
import pandas as pd

from datetime import datetime as dt


def pre_tag_to_json(html_source):
    return json.loads(html_source.find("pre").text)


def json_dump(obj):
    print(json.dumps(obj, indent=2))


def create_file(folder_name, name, timestamp=True):
    now = dt.now()
    format_timestamp = now.strftime("%Y%m%d%H%M%S")

    dir_path = os.path.join(os.getcwd(), "output", folder_name)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_name = f"{format_timestamp}-{name}" if timestamp else f"{name}"
    file_path = os.path.join(dir_path, file_name)

    return file_path


def create_json_file(file_name, data, timestamp=True):
    with open(create_file("temp", file_name, timestamp), "w") as file:
        jsonString = json.dumps(data)
        file.write(jsonString)


def create_csv_file(file_name, df, timestamp=True):
    df_path = create_file("csv", file_name, False)
    df.to_csv(df_path)

    return df


def get_last_page(obj):
    return obj["paging"]["last_page"]
