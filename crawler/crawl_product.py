import json
import pandas as pd

from source.driver import create_driver
from source.constant import (
    URL_PRODUCT_LIST,
    URL_PRODUCT_PAGE,
    URL_PRODUCT_BY_SELLER,
    URL_PRODUCT_DETAIL,
    URL_PRODUCT_CHILD_BY_SELLER,
    URL_REVIEW,
)
from source.utils import (
    pre_tag_to_json,
    json_dump,
    create_csv_file,
    create_csv_file_filter,
)

from source.tables import (
    TABLE_PRODUCT,
    TABLE_PRODUCT_COLUMNS,
    TABLE_PRODUCT_DETAIL,
    TABLE_PRODUCT_DETAIL_COLUMNS,
)

# Get Product List Page
print(f"Crawling Product Page: {URL_PRODUCT_LIST}")
prod_list_driver, prod_list_soup = create_driver(URL_PRODUCT_LIST)
prod_list_json = pre_tag_to_json(prod_list_soup)

# Get Seller and Brand
prod_list_filters = prod_list_json["filters"]
for pl_filter in prod_list_filters:

    file_location = create_csv_file_filter("locations.csv", "stock_location", pl_filter)

    file_brand = create_csv_file_filter(
        "brands.csv",
        "brand",
        pl_filter,
        convert_to_number=True,
    )

    if file_brand is not None:
        dict_brand = file_brand

    file_color = create_csv_file_filter("colors.csv", "option_color", pl_filter)

    file_seller = create_csv_file_filter(
        "sellers.csv",
        "seller",
        pl_filter,
        convert_to_number=True,
    )
    if file_seller is not None:
        sellers = file_seller

# total_prods = 0

# for seller in sellers:
#     break
#     seller_id = seller["id"]

#     prod_by_seller_driver, prod_by_seller_soup = create_driver(
#         "https://api.tiki.vn/seller-store/v2/collections/5/products?seller_id=1&limit=100&cursor=0&category=1795"
#     )
#     # prod_by_seller_driver, prod_by_seller_soup = create_driver(URL_PRODUCT_BY_SELLER)
#     prod_by_seller_json = pre_tag_to_json(prod_by_seller_soup)

#     print(prod_by_seller_json)

#     # total_prod = prod_by_seller_json["page"]["total"]
#     # print(total_prod)
#     # total_prods += total_prod

# print(total_prods)

# # Get Products
prod_last_page = prod_list_json["paging"]["last_page"] + 1

df_products = pd.DataFrame(columns=TABLE_PRODUCT_COLUMNS)
df_product_details = pd.DataFrame(columns=TABLE_PRODUCT_DETAIL_COLUMNS)

for prod_page in range(1, prod_last_page):
    print(f"Crawling Product Page: {URL_PRODUCT_PAGE.format(prod_page)}")
    prod_page_drive, prod_page_soup = create_driver(URL_PRODUCT_PAGE.format(prod_page))
    prod_page_data = pre_tag_to_json(prod_page_soup)["data"]

    for prod in prod_page_data:
        try:
            prod_id = prod["id"]
            prod_db_row = {}

            print(f"Crawling Product Detail: {prod_id}")
            prod_detail_driver, prod_detail_soup = create_driver(
                URL_PRODUCT_DETAIL.format(prod_id)
            )
            prod_detail = pre_tag_to_json(prod_detail_soup)

            prod_detail_atts = [
                pd["attributes"]
                for pd in prod_detail["specifications"]
                if pd["name"] == "Content"
            ][0]

            for key in TABLE_PRODUCT:
                prod_key = TABLE_PRODUCT[key]

                if prod.get(prod_key):
                    prod_value = prod[prod_key]
                    prod_db_row[key] = [prod_value]

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
                    prod_child_db_row["product_id"] = [prod_id]
                    prod_child_db_row["color"] = [prod_child["option1"]]
                    prod_child_db_row["seller_id"] = [pd_by_seller["seller"]["id"]]
                    prod_child_db_row["store_id"] = [pd_by_seller["seller"]["store_id"]]
                    prod_child_db_row["price"] = [pd_by_seller["price"]["value"]]

                    df_prod_child_db_row = pd.DataFrame(prod_child_db_row)
                    df_product_details = pd.concat(
                        [df_product_details, df_prod_child_db_row], ignore_index=True
                    )

                # Product review

        except Exception as e:
            print(e)
            continue

create_csv_file("products.csv", df_products)
create_csv_file("product_details.csv", df_product_details)
