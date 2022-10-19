import json
import pandas as pd

from source.driver import create_driver_request, create_driver
from source.utils import json_dump, df_read_csv, create_csv_file, pre_tag_to_json
from source.constant import (
    URL_PRODUCT_BY_SELLER,
    URL_PRODUCT_DETAIL,
    URL_PRODUCT_CHILD_BY_SELLER,
)
from source.tables import TABLE_PRODUCT

products_csv = "output/csv/products.csv"
product_details_csv = "output/csv/product_details.csv"
sellers_csv = "output/csv/sellers.csv"
brands_csv = "output/csv/brands.csv"
products = pd.read_csv(products_csv).to_dict("records")
sellers = pd.read_csv(sellers_csv).to_dict("records")
brands = pd.read_csv(brands_csv).to_dict("records")

df_brands = df_read_csv(brands_csv)
df_products = df_read_csv(products_csv)
df_product_details = df_read_csv(product_details_csv)

new_products = []
new_brands = []
new_brands_dict = []

for seller in sellers:
    seller_id = seller["id"]

    products_by_seller = create_driver_request(URL_PRODUCT_BY_SELLER.format(seller_id))
    products_per_page = products_by_seller["data"]
    total_products_per_page = len(products_per_page)
    total_products = products_by_seller["page"]["total"]

    for ppp in products_per_page:
        product_exists = False
        brand_exists = False

        for product in products:
            if product["id"] == ppp["id"]:
                product_exists = True

        for brand in brands:
            if ppp["brand_id"] == brand["id"]:
                brand_exists = True

        if product_exists == False and ppp["id"] not in new_products:
            new_products.append(ppp["id"])

        if brand_exists == False and ppp["brand_id"] not in new_brands:
            new_brands.append(ppp["brand_id"])
            df_brand_new = pd.DataFrame(
                [
                    {"id": ppp["brand_id"], "name": ppp["brand_name"]},
                ]
            )
            df_brands = pd.concat([df_brands, df_brand_new], ignore_index=True)
            # new_brands_dict.append({"id": ppp["brand_id"], "name": ppp["brand_name"]})

for index, new_product in enumerate(new_products):
    product_index = index + 1
    prod_db_row = {}
    prod_detail = create_driver_request(URL_PRODUCT_DETAIL.format(new_product))

    try:

        print(f"Crawling: {new_product} - {product_index}/{len(new_products)}")
        prod_detail_atts = [
            pd["attributes"]
            for pd in prod_detail["specifications"]
            if pd["name"] == "Content"
        ][0]

        for key in TABLE_PRODUCT:
            prod_key = TABLE_PRODUCT[key]

            # if prod.get(prod_key):
            #     prod_value = prod[prod_key]
            #     prod_db_row[key] = [prod_value]

            if prod_detail.get(prod_key):
                prod_value = prod_detail[prod_key]
                prod_db_row[key] = [prod_value]

            for prod_detail_att in prod_detail_atts:
                if prod_detail_att["code"] == prod_key:
                    prod_db_row[key] = [prod_detail_att["value"]]

            if prod_db_row.get(key) is None:
                prod_db_row[key] = "N/A"

        df_prod_db_row = pd.DataFrame(prod_db_row)
        df_products = pd.concat([df_products, df_prod_db_row], ignore_index=True)

        prod_childs = prod_detail["configurable_products"]
        prod_child_db_row = {}

        for prod_child in prod_childs:
            prod_child_id = prod_child["id"]

            # Product detail
            print(f"Crawling Product Child: {prod_child_id}")
            prod_child_driver, prod_child_soup = create_driver(
                URL_PRODUCT_CHILD_BY_SELLER.format(prod_child_id)
            )

            prod_child_data = pre_tag_to_json(prod_child_soup)
            prod_child_by_sellers = prod_child_data["all_sellers"]

            for pd_by_seller in prod_child_by_sellers:
                prod_child_db_row["id"] = [prod_child_id]
                prod_child_db_row["product_id"] = [new_product]
                prod_child_db_row["color"] = [prod_child["option1"]]
                prod_child_db_row["seller_id"] = [pd_by_seller["seller"]["id"]]
                prod_child_db_row["store_id"] = [pd_by_seller["seller"]["store_id"]]
                prod_child_db_row["price"] = [pd_by_seller["price"]["value"]]

                df_prod_child_db_row = pd.DataFrame(prod_child_db_row)
                df_product_details = pd.concat(
                    [df_product_details, df_prod_child_db_row], ignore_index=True
                )

    except Exception as e:
        print(e)

    break

print(df_products)

# create_csv_file("brands_new.csv", df_brands)
# create_csv_file("products_new.csv", df_products)
# create_csv_file("product_details_new.csv", df_product_details)
