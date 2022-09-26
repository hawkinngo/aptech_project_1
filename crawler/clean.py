import json
import pandas as pd

from source.tables import (
    BRANDS_COLUMNS,
    SELLERS_COLUMNS,
    PRODUCTS_COLUMNS,
    PRODUCT_DETAILS_COLUMNS,
    PRODUCTS,
    PRODUCT_DETAILS,
)
from source.utils import json_dump, create_csv_file

# Create file path
# product_csv = create_csv_file("products.csv", PRODUCTS_COLUMNS, False)
# seller_csv = create_csv_file("seller.csv", SELLERS_COLUMNS, False)
# brand_csv = create_csv_file("brand.csv", BRANDS_COLUMNS, False)
# detail_csv = create_csv_file("product_detail.csv", PRODUCT_DETAILS_COLUMNS, False)

# Data
df_products = pd.DataFrame(columns=PRODUCTS_COLUMNS)

products_file = open("output/temp/products.json")
product_details_file = open("output/temp/product_details.json")
product_sellers_file = open("output/temp/product_sellers.json")
reviews_file = open("output/temp/reviews.json")

products = json.load(products_file)
product_details = json.load(product_details_file)
product_sellers = json.load(product_sellers_file)
reviews = json.load(reviews_file)

json_dump(reviews[0])

for index, product in enumerate(products):
    product_db_item = {}
    product_id = product["id"]
    product_detail = product_details[index]
    product_atts = [
        pd["attributes"]
        for pd in product_detail["specifications"]
        if pd["name"] == "Content"
    ][0]

    for key in PRODUCTS:
        product_key = PRODUCTS[key]

        if product.get(product_key):
            product_value = product[product_key]
            product_db_item[key] = [product_value]

        if product_detail.get(product_key):
            product_value = product_detail[product_key]
            product_db_item[key] = [product_value]

        for product_att in product_atts:
            if product_att["code"] == product_key:
                product_db_item[key] = [product_att["value"]]

        # if product_key == "quantity_store":
        # print(product_detail["stock_item"]["qty"])

        if product_db_item.get(key) is None:
            product_db_item[key] = "N/A"

    # json_dump(product_db_item)
    # print(product_atts)

    # for product_detail in product_details:
    #     print(product_detail["id"])
    df_product_db_item = pd.DataFrame(product_db_item)

    df_products = pd.concat([df_products, df_product_db_item], ignore_index=True)

    if index == 1:
        break

create_csv_file("products.csv", df_products, False)
