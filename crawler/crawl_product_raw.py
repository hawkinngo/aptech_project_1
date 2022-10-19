import json
import math
import pandas as pd

from pprint import pprint
from source.driver import create_driver_request
from source.utils import create_csv_file_filter, create_csv_file
from source.constant import (
    URL_PRODUCT_LIST,
    URL_PRODUCT_BY_BRAND,
    URL_PRODUCT_DETAIL,
    PRODUCTS_RAW_FILE,
)
from source.tables import TABLE_PRODUCT

tiki = create_driver_request(URL_PRODUCT_LIST)
tiki_filters = tiki["filters"]

brands = {}
sellers = {}

product_rows = []

for tiki_filter in tiki_filters:

    create_csv_file_filter("locations.csv", "stock_location", tiki_filter)

    create_csv_file_filter("colors.csv", "option_color", tiki_filter)

    create_csv_file_filter("storages.csv", "filter_mobile_rom", tiki_filter)

    create_csv_file_filter("rams.csv", "filter_mobile_ram", tiki_filter)

    create_brands_file = create_csv_file_filter(
        "brands.csv",
        "brand",
        tiki_filter,
        convert_to_number=True,
    )

    if create_brands_file is not None:
        brands = create_brands_file

    create_sellers_file = create_csv_file_filter(
        "sellers.csv",
        "seller",
        tiki_filter,
        convert_to_number=True,
    )

    if create_sellers_file is not None:
        sellers = create_sellers_file


for brand in brands:
    brand_id = brand["id"]
    brand_name = brand["name"]
    total_product = brand["total_product"]
    total_page = math.ceil(total_product / 100)
    print(f"\n{brand_name} - {total_product} products")

    # if brand_id != 112735:
    #     continue

    for page in range(1, total_page + 1):
        products_by_seller = create_driver_request(
            URL_PRODUCT_BY_BRAND.format(brand_id, page)
        )
        products = products_by_seller["data"]

        for product in products:
            product_id = product["id"]
            product_name = product["name"]
            product_row = {}
            print(f"Crawling {product_id} - {product_name}\n")

            try:
                product_detail = create_driver_request(
                    URL_PRODUCT_DETAIL.format(product_id)
                )
            except:
                product_detail = create_driver_request(
                    URL_PRODUCT_DETAIL.format(product_id)
                )

            product_detail_attrs = [
                pd["attributes"]
                for pd in product_detail["specifications"]
                if pd["name"] == "Content" or pd["name"] == "Thông tin chung"
            ][0]

            for key in TABLE_PRODUCT:
                product_key = TABLE_PRODUCT[key]

                if product.get(product_key):
                    product_value = product[product_key]
                    product_row[key] = product_value

                if product_detail.get(product_key):
                    product_value = product_detail[product_key]
                    product_row[key] = product_value

                for product_detail_attr in product_detail_attrs:
                    if product_detail_attr["code"] == product_key:
                        product_row[key] = product_detail_attr["value"]

                if product_row.get(key) is None:
                    product_row[key] = "NaN"

            product_rows.append(product_row)

df_products = pd.DataFrame(product_rows)
create_csv_file(PRODUCTS_RAW_FILE, df_products)

# products = []
# products_dict = []
# brands = []
# brands_dict = []

# for seller in sellers:
#     seller_id = seller["id"]

#     products_by_seller = create_driver_request(URL_PRODUCT_BY_SELLER.format(seller_id))

#     products_data = products_by_seller["data"]

#     for product in products_data:

#         if product["id"] not in products:
#             products.append(product["id"])

#         # if product["brand_id"] not in brands:
#         #     brands.append(product["brand_id"])
#         #     brands_dict.append(
#         #         {
#         #             "id": product["brand_id"],
#         #             "name": product["brand_name"],
#         #         }
#         #     )

#         product_row = {
#             "product_id": product["id"],
#             "seller_id": seller_id,
#             "original_price": product["original_price"],
#             "quantity_sold": product["quantity_sold"]["value"]
#             if product.get("quantity_sold") is not None
#             else "N/A",
#             "total_reviews": product["review_count"],
#             "total_review_pages": math.ceil(product["review_count"] / 20),
#         }
#         products_dict.append(product_row)

# # df_brands = pd.DataFrame(brands_dict)
# # create_csv_file("brands.csv", df_brands)

# df_product_sellers = pd.DataFrame(products_dict)
# create_csv_file("product_sellers.csv", df_product_sellers)

# # for product in products:
