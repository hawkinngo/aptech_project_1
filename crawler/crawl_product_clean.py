import json
import pandas as pd

from pprint import pprint
from source.constant import (
    PRODUCTS_RAW_FILE,
    OUTSOURCE_PATH,
    PRODUCTS_FILTER_FILE,
    STORAGES_FILE,
    RAMS_FILE,
    RAM_REPLACE,
    STORAGE_REPLACE,
    COLORS_FILE,
    PRODUCTS_DETAIL_LV1,
    FILTER_CLEAN,
    CLEANSOURCE_PATH,
    PRODUCTS_FILE,
    BRANDS_FILE,
    SELLERS_FILE,
)
from source.utils import (
    df_read_csv,
    create_csv_file,
    filter_spam_name,
    check_product_name,
)

brands_csv = OUTSOURCE_PATH.format(BRANDS_FILE)
sellers_csv = OUTSOURCE_PATH.format(SELLERS_FILE)
products_raw_csv = OUTSOURCE_PATH.format(PRODUCTS_RAW_FILE)
storages_csv = OUTSOURCE_PATH.format(STORAGES_FILE)
rams_csv = OUTSOURCE_PATH.format(RAMS_FILE)
colors_csv = OUTSOURCE_PATH.format(COLORS_FILE)

#
df_brands_raw = df_read_csv(brands_csv)
brands_raw = df_brands_raw.to_dict("records")

df_sellers_raw = df_read_csv(sellers_csv)
sellers_raw = df_sellers_raw.to_dict("records")

df_products_raw = df_read_csv(products_raw_csv)
products_raw = df_products_raw.to_dict("records")

df_storages = df_read_csv(storages_csv)
df_storages.sort_values(by="number", ascending=False, inplace=True)
storages = df_storages.to_dict("records")

df_rams = df_read_csv(rams_csv)
df_rams.sort_values(by="number", ascending=False, inplace=True)
rams = df_rams.to_dict("records")

df_colors = df_read_csv(colors_csv)
df_colors["name"] = df_colors["name"].str.title()
df_colors.sort_values(by="name", inplace=True)
colors = df_colors.to_dict("records")
colors_name = [color["name"] for color in colors]

products_filter = []

configurables = {"yes": 0, "no": 0, "color": 0, "double": 0}

brand_cleans = []
for brand_raw in brands_raw:
    del brand_raw["total_product"]
    brand_cleans.append(brand_raw)


for product_raw in products_raw:
    product_id = product_raw["id"]
    product_name = product_raw["name"]

    if "gift" in product_name.lower():
        continue

    if "spen" in product_name.lower():
        continue

    check_product = check_product_name(product_name)

    product_raw["is_genuine"] = check_product["is_genuine"]
    product_raw["is_second_hand"] = check_product["is_second_hand"]
    product_raw["is_imported_goods"] = check_product["is_imported_goods"]

    if isinstance(product_raw["storage_capacity"], str) is False:
        if isinstance(product_raw["storage_capacity2"], str) is True:
            product_raw["storage_capacity"] = product_raw["storage_capacity2"]
        else:
            for i, storage in enumerate(storages):
                if storage["name"] in product_name:
                    product_raw["storage_capacity"] = storage["name"]

                    product_raw["name"] = product_raw["name"].replace(
                        storage["name"], ""
                    )
                    break

    if isinstance(product_raw["ram"], str) is False:
        for i, ram in enumerate(rams):
            if ram["name"] in product_name:
                product_raw["ram"] = ram["name"]

                product_raw["name"] = product_raw["name"].replace(ram["name"], "")
                break

    if (
        isinstance(product_raw["ram"], float) is False
        and isinstance(product_raw["storage_capacity"], float) is False
    ):
        try:
            if int(product_raw["ram"].replace("GB", "")) > int(
                product_raw["storage_capacity"].replace("GB", "")
            ):
                temp = product_raw["ram"]
                product_raw["ram"] = product_raw["storage_capacity"]
                product_raw["storage_capacity"] = temp
        except:
            pass

    if isinstance(product_raw["ram"], float) is False:
        # print(product_raw["battery_type"])
        for key in RAM_REPLACE:
            product_raw["ram"] = product_raw["ram"].replace(key, RAM_REPLACE[key])

        product_raw["ram"] = product_raw["ram"].strip()
        if "GB" not in product_raw["ram"]:
            product_raw["ram"] = f"{product_raw['ram']}GB"
        print(product_raw["ram"], type(product_raw["ram"]))

    if isinstance(product_raw["storage_capacity"], float) is False:
        # print(product_raw["battery_type"])
        for key in STORAGE_REPLACE:
            product_raw["storage_capacity"] = product_raw["storage_capacity"].replace(
                key, STORAGE_REPLACE[key]
            )

        product_raw["storage_capacity"] = product_raw["storage_capacity"].strip()
        if "GB" not in product_raw["storage_capacity"]:
            product_raw["storage_capacity"] = f"{product_raw['storage_capacity']}GB"
        print(product_raw["storage_capacity"], type(product_raw["storage_capacity"]))

    if product_raw["storage_capacity"] == "-GB":
        product_raw["storage_capacity"] = "NaN"
    product_raw["name"] = filter_spam_name(product_name)
    products_filter.append(product_raw)

    if "Samsung" in product_raw["name"] and "Samsung Galaxy" not in product_raw["name"]:
        product_raw["name"] = product_raw["name"].replace("Samsung", "Samsung Galaxy")

    for color_name in colors_name:
        if color_name in product_raw["name"]:
            configurables["color"] = configurables["color"] + 1
            if isinstance(product_raw["configurable_products"], str) is True:
                configurables["double"] = configurables["double"] + 1
            break

    if isinstance(product_raw["configurable_products"], str) is False:
        configurables["no"] = configurables["no"] + 1
    else:
        configurables["yes"] = configurables["yes"] + 1


df_products_filter = pd.DataFrame(products_filter)
create_csv_file(PRODUCTS_FILTER_FILE, df_products_filter)

products_clean = {
    "name": [],
    "brand_id": [],
    "original_price": [],
    "ram": [],
    "storage_capacity": [],
}

for product in products_filter:
    # product_name = product["name"]
    product_name_clean = product["name"]

    for filter_clean in FILTER_CLEAN:
        product_name_clean = (
            product_name_clean.replace(filter_clean, "").replace("  ", " ").strip()
        )

    for filter_colors in colors_name:
        product_name_clean = (
            product_name_clean.replace(filter_colors, "")
            .replace("Nhạt", "")
            .replace("Đậm", "")
            .replace("Thạch Anh", "")
            .replace("on 19 Pro", "Camon 19 Pro")
            .replace("CamCamCamCamCamCamCamCamCamCamCamCamCam", "Cam")
            .replace("  ", " ")
            .strip()
        )

    if product_name_clean not in products_clean["name"]:
        products_clean["name"].append(product_name_clean)
        products_clean["brand_id"].append(product["brand_id"])
        products_clean["original_price"].append(product["price"])
        products_clean["ram"].append(product["ram"])
        products_clean["storage_capacity"].append(product["storage_capacity"])


# CLEAN DATA
df_brand_cleans = pd.DataFrame(brand_cleans).sort_values(by="id")
create_csv_file(BRANDS_FILE, df_brand_cleans, is_clean=True)

df_color_cleans = pd.DataFrame(df_colors).sort_values(by="id")
create_csv_file(COLORS_FILE, df_color_cleans, is_clean=True)

df_seller_cleans = pd.DataFrame(df_sellers_raw).sort_values(by="id")
create_csv_file(SELLERS_FILE, df_seller_cleans, is_clean=True)

df_product_name_cleans = (
    pd.DataFrame(products_clean).sort_values(by="name").reset_index(drop=True)
)
df_product_name_cleans.index += 1
pd.set_option("display.max_rows", None)
print(df_product_name_cleans)
create_csv_file(PRODUCTS_FILE, df_product_name_cleans, is_clean=True)

# checker = {}

# for product in products_filter:
#     # print(product)
#     product_name = product["name"]

#     checker[product["id"]] = []

#     for product_compare in products_filter:
#         if (
#             product["id"] == product_compare["id"]
#             or checker.get(product_compare["id"]) is not None
#         ):
#             continue

#         product_name_compare = product_compare["name"]

#         check = difflib.SequenceMatcher(None, product_name, product_name_compare)

#         if check.ratio() == 1:
#             checker[product["id"]].append(product_compare["id"])

#     # if len(checker[product["id"]]) == 0:
#     #     del checker[product["id"]]
#     #     total_single += 1
#     # else:
#     #     total_checker += len(checker[product["id"]])

# for key in checker:
#     aaa = [key] + checker[key]
#     df_checker = df_products_filter[df_products_filter["id"].isin(aaa)]

#     for index, row in df_checker.iterrows():
#         # if row["brand_id"] != 25422:
#         # continue
#         row_name = row["name"]

#         for filter_clean in FILTER_CLEAN:
#             row_name = row_name
#             row_name = row_name.replace(filter_clean, "").replace("  ", " ").strip()

#         print(row["id"], row_name)

# print("\n")

# df_checker.reset_index(inplace=True)

# print(df_checker.iterrows())

# for index, row in df_checker.iterrows():

# print(row["name"])
# print(row.iat[0, 0], "---", row.iat[0, 3])
