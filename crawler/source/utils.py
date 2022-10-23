import json
import os
import pandas as pd
import re

from datetime import datetime as dt
from .constant import FILTER_LIST, REPLACE_PRODUCT_NAME


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

    print(f"{file_name} is created")
    return file_path


def create_json_file(file_name, data, timestamp=True):
    with open(create_file("temp", file_name, timestamp), "w") as file:
        jsonString = json.dumps(data)
        file.write(jsonString)


def create_csv_file(
    file_name, df, convert_to_number=False, timestamp=False, is_clean=False
):
    df_path = create_file("csv" if is_clean is False else "clean", file_name, timestamp)
    # df_path = create_file("csv", file_name, False)
    df.to_csv(df_path)

    return df.to_dict("records")


def create_csv_file_filter(
    filter_file_name, filter_name, filter_state, convert_to_number=False
):
    if filter_state["query_name"] == filter_name:
        df_filters = pd.DataFrame(columns=["id", "name"])
        row_filter = {}

        for one_filter in filter_state["values"]:
            row_filter["id"] = (
                [int(one_filter["query_value"])]
                if convert_to_number
                else [one_filter["query_value"]]
            )
            row_filter["name"] = [one_filter["display_value"]]

            if filter_state["query_name"] == "seller":
                row_filter["address"] = [one_filter["seller_address"]]

            if filter_state["query_name"] == "brand":
                row_filter["total_product"] = [one_filter["count"]]

            if (
                filter_state["query_name"] == "filter_mobile_rom"
                or filter_state["query_name"] == "filter_mobile_ram"
            ):
                filter_value = (
                    float(one_filter["display_value"][:-2])
                    if one_filter["display_value"][-2:] == "GB"
                    else float(one_filter["display_value"][:-2]) / 1000
                )

                row_filter["number"] = [filter_value]

            df_row_filter = pd.DataFrame(row_filter)
            df_filters = pd.concat([df_filters, df_row_filter], ignore_index=True)

        create_csv_file(filter_file_name, df_filters, False)

        return df_filters.to_dict("records")
    return None


def get_last_page(obj):
    return obj["paging"]["last_page"]


def df_read_csv(csv_file_path):
    try:
        df_csv = pd.read_csv(csv_file_path)
        first_column = df_csv.columns[0]
        df_csv = df_csv.drop([first_column], axis=1)
        return df_csv
    except Exception as exp:
        print(exp)
        return False


def check_product_name(str_input):
    str_input = str_input.lower()
    result = {}

    result["is_genuine"] = True if "hàng chính hãng" in str_input else False

    result["is_second_hand"] = True if "đã kích hoạt" in str_input else False

    result["is_imported_goods"] = (
        True if "hàng nhập khẩu" in str_input or "quốc tế" in str_input else False
    )

    return result


def filter_spam_name(str_input):
    filter_str = str_input

    for one_filter in FILTER_LIST:
        if one_filter == " l ":
            filter_str = filter_str.replace(one_filter, "/")
        else:
            filter_str = filter_str.replace(one_filter, "")

    clean_str = filter_str.strip().title()

    result = " ".join(clean_str.split())

    for key in REPLACE_PRODUCT_NAME:
        result = result.replace(key, REPLACE_PRODUCT_NAME[key])

    return result
