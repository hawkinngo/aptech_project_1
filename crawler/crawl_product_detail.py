import difflib
import json
import pandas as pd
from pprint import pprint

from source.driver import create_driver_request

from source.utils import df_read_csv, create_csv_file

from source.constant import (
    URL_PRODUCT_CHILD_BY_SELLER,
    CLEANSOURCE_PATH,
    OUTSOURCE_PATH,
    PRODUCTS_FILTER_FILE,
    COLORS_FILE,
    PRODUCTS_FILE,
    PRODUCT_DETAILS_FILE,
    REVIEWS_FILE,
    FILTER_CLEAN,
    COLOR_FILTER_SILVER,
    COLOR_FILTER_GREY,
    COLOR_FILTER_BLUE,
    COLOR_FILTER_WHITE,
    COLOR_FILTER_BLACK,
)

product_filters_csv = OUTSOURCE_PATH.format(PRODUCTS_FILTER_FILE)
df_product_filters = df_read_csv(product_filters_csv)
product_filters = df_product_filters.to_dict("records")

product_cleans_csv = CLEANSOURCE_PATH.format(PRODUCTS_FILE)
df_product_cleans = df_read_csv(product_cleans_csv)
product_cleans = df_product_cleans.to_dict("records")

colors_csv = OUTSOURCE_PATH.format(COLORS_FILE)
df_colors = df_read_csv(colors_csv)
df_colors.sort_values(by="name", ascending=False, inplace=True)
colors = df_colors.to_dict("records")
colors_name = [color["name"] for color in colors]

reviews_csv = OUTSOURCE_PATH.format(REVIEWS_FILE)
df_reviews = df_read_csv(reviews_csv)
reviews = df_reviews.to_dict("records")

product_matches = {}

for product_index, product_clean in enumerate(product_cleans, start=1):

    product_clean_name = product_clean["name"]

    product_matches[product_index] = []

    for product_filter in product_filters:
        product_name = product_filter["name"]

        for filter_clean in FILTER_CLEAN:
            product_name = (
                product_name.replace(filter_clean, "").replace("  ", " ").strip()
            )

        for filter_colors in colors_name:
            product_name = (
                product_name.replace(filter_colors.title(), "")
                .replace("Nhạt", "")
                .replace("Đậm", "")
                .replace("Thạch Anh", "")
                .replace("on 19 Pro", "Camon 19 Pro")
                .replace("  ", " ")
                .strip()
            )

        check = difflib.SequenceMatcher(None, product_clean_name, product_name)

        if check.ratio() == 1:
            product_matches[product_index].append(product_filter["id"])


product_details = []

for i in product_matches:
    product_id_list = product_matches[i]
    df_product_matches = df_product_filters[
        df_product_filters["id"].isin(product_id_list)
    ]

    for product_index, product_row in df_product_matches.iterrows():
        # print(product_row)
        configurable_products = product_row["configurable_products"]

        if isinstance(configurable_products, str) is True:
            configurable_clean = (
                configurable_products.replace('"', "inch")
                .replace("'", '"')
                .replace("False", '"False"')
                .replace("True", '"True"')
            )

            configurables = json.loads(configurable_clean)
            for configurable in configurables:
                product_detail_row = {}
                is_checked = False
                color_clean = ""
                option_color = configurable["option1"].title()

                if option_color in COLOR_FILTER_SILVER:
                    color_clean = "Bạc"
                    is_checked = True

                if option_color in COLOR_FILTER_GREY:
                    color_clean = "Xám"
                    is_checked = True

                if option_color in COLOR_FILTER_BLUE:
                    color_clean = "Xanh Dương"
                    is_checked = True

                if option_color in COLOR_FILTER_WHITE:
                    color_clean = "Trắng"
                    is_checked = True

                if option_color in COLOR_FILTER_BLACK:
                    color_clean = "Đen"
                    is_checked = True

                if is_checked is False:
                    for filter_color in colors_name:
                        if filter_color in configurable["option1"]:
                            color_clean = filter_color
                            is_checked = True
                            break

                sellers = create_driver_request(
                    URL_PRODUCT_CHILD_BY_SELLER.format(configurable["id"])
                )["all_sellers"]

                product_detail_row["product_id"] = i
                product_detail_row["product_id_crawl"] = product_row["id"]
                product_detail_row["product_detail_id"] = configurable["id"]
                product_detail_row["color"] = color_clean
                product_detail_row["is_genuine"] = product_row["is_genuine"]
                product_detail_row["is_used"] = product_row["is_second_hand"]
                product_detail_row["is_imported_goods"] = product_row[
                    "is_imported_goods"
                ]

                for seller in sellers:
                    product_detail_row["seller"] = seller["seller"]["id"]
                    product_detail_row["sell_price"] = (
                        seller["price"]["value"]
                        if product_row["price"] >= seller["price"]["value"]
                        else product_row["price"]
                    )
                    product_details.append(product_detail_row)
        else:
            product_sub_id = product_row["url"].split("=")[1]

            product_detail_row["product_id"] = i
            product_detail_row["product_id_crawl"] = product_row["id"]
            product_detail_row["product_detail_id"] = product_sub_id
            product_detail_row["is_genuine"] = product_row["is_genuine"]
            product_detail_row["is_used"] = product_row["is_second_hand"]
            product_detail_row["is_imported_goods"] = product_row["is_imported_goods"]
            color_clean = ""

            for filter_color in colors_name:
                if filter_color in product_row["name"]:
                    color_clean = filter_color
                    break

            if color_clean == "":
                for filter_color in COLOR_FILTER_SILVER:
                    if filter_color in product_row["name"]:
                        color_clean = filter_color
                        break

            if color_clean == "":
                for filter_color in COLOR_FILTER_BLACK:
                    if filter_color in product_row["name"]:
                        color_clean = filter_color
                        break

            if color_clean == "":
                for filter_color in COLOR_FILTER_GREY:
                    if filter_color in product_row["name"]:
                        color_clean = filter_color
                        break

            if color_clean == "":
                for filter_color in COLOR_FILTER_BLUE:
                    if filter_color in product_row["name"]:
                        color_clean = filter_color
                        break

            if color_clean == "":
                for filter_color in COLOR_FILTER_WHITE:
                    if filter_color in product_row["name"]:
                        color_clean = filter_color
                        break

            product_detail_row["color"] = color_clean

            sellers = create_driver_request(
                URL_PRODUCT_CHILD_BY_SELLER.format(product_sub_id)
            )["all_sellers"]

            for seller in sellers:
                product_detail_row["seller"] = seller["seller"]["id"]
                product_detail_row["sell_price"] = seller["price"]["value"]
                product_details.append(product_detail_row)

print(product_details)

df_product_details = pd.DataFrame(product_details)
create_csv_file(PRODUCT_DETAILS_FILE, df_product_details, is_clean=True)

reviews_clean = []

# for review in reviews:

#     get_product = df_product_filters[df_product_filters["id"] == review["product_id"]]

#     brand_id = get_product["brand_id"].values[0]
#     product_name = get_product["name"].values[0]

#     for filter_clean in FILTER_CLEAN:
#         product_name = product_name.replace(filter_clean, "").replace("  ", " ").strip()

#     for filter_colors in colors_name:
#         product_name = (
#             product_name.replace(filter_colors.title(), "")
#             .replace("Nhạt", "")
#             .replace("Đậm", "")
#             .replace("Thạch Anh", "")
#             .replace("on 19 Pro", "Camon 19 Pro")
#             .replace("  ", " ")
#             .strip()
#         )

#     product_index = df_product_cleans[
#         (df_product_cleans["brand_id"] == brand_id)
#         & (df_product_cleans["name"] == product_name)
#     ].index.values[0]

#     if review["product_id"] == 29931445:
#         print(product_name)
#         print(product_index)

#     review["id"] = product_index
#     reviews_clean.append(review)

# df_reviews_clean = pd.DataFrame(reviews_clean)

# df_reviews_clean = df_reviews_clean.groupby(
#     [
#         "product_id",
#         "product_detail_id",
#         "seller_id",
#         "id",
#     ]
# ).sum()

# create_csv_file(REVIEWS_FILE, df_reviews_clean, is_clean=True)

# print(df_reviews_clean)
