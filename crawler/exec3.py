import json
import pandas as pd
import csv

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
    TABLE_REVIEW,
    TABLE_REVIEW_COLUMNS,
)

products_csv = "output/csv/products.csv"
sellers_csv = "output/csv/sellers.csv"


products = pd.read_csv(products_csv).to_dict("records")
sellers = pd.read_csv(sellers_csv).to_dict("records")

df_reviews = pd.DataFrame(columns=TABLE_REVIEW_COLUMNS)

for product in products:
    break
    prod_id = product["id"]

    for seller in sellers:
        seller_id = seller["id"]

        review_driver, review_soup = create_driver(
            URL_REVIEW.format(1, prod_id, seller_id)
        )

        review_data = pre_tag_to_json(review_soup)
        review_total = review_data["paging"]["total"]
        review_last_page = pre_tag_to_json(review_soup)["paging"]["last_page"] + 1

        review_db_row = {}

        if review_total > 0:
            count_reviews = {}
            for review_page in range(1, review_last_page):
                print(
                    f"Crawling seller_id {seller_id} - page {review_page}, product_id {prod_id}"
                )
                review_driver, review_soup = create_driver(
                    URL_REVIEW.format(review_page, prod_id, seller_id)
                )
                reviews = pre_tag_to_json(review_soup)["data"]

                for index, review in enumerate(reviews):
                    child_id = review["spid"]
                    rating = review["rating"]

                    if count_reviews.get(child_id) is None:
                        count_reviews[child_id] = {
                            "rating_1": 0,
                            "rating_2": 0,
                            "rating_3": 0,
                            "rating_4": 0,
                            "rating_5": 0,
                        }

                    if rating == 1:
                        count_reviews[child_id]["rating_1"] += 1
                    if rating == 2:
                        count_reviews[child_id]["rating_2"] += 1
                    if rating == 3:
                        count_reviews[child_id]["rating_3"] += 1
                    if rating == 4:
                        count_reviews[child_id]["rating_4"] += 1
                    if rating == 5:
                        count_reviews[child_id]["rating_5"] += 1

                review_db_row["product_id"] = [prod_id]
                review_db_row["seller_id"] = [seller_id]

            for key in count_reviews:
                count_review = count_reviews[key]
                review_db_row["child_id"] = [key]
                review_db_row["rating_1"] = [count_review["rating_1"]]
                review_db_row["rating_2"] = [count_review["rating_2"]]
                review_db_row["rating_3"] = [count_review["rating_3"]]
                review_db_row["rating_4"] = [count_review["rating_4"]]
                review_db_row["rating_5"] = [count_review["rating_5"]]

                df_review_db_row = pd.DataFrame(review_db_row)
                df_reviews = pd.concat(
                    [df_reviews, df_review_db_row], ignore_index=True
                )

print(df_reviews)
#     for prod in prod_page_data:
#         try:
#             prod_id = prod["id"]
#             prod_db_row = {}

#             print(f"Crawling Product Detail: {prod_id}")
#             prod_detail_driver, prod_detail_soup = create_driver(
#                 URL_PRODUCT_DETAIL.format(prod_id)
#             )
#             prod_detail = pre_tag_to_json(prod_detail_soup)

#             prod_detail_atts = [
#                 pd["attributes"]
#                 for pd in prod_detail["specifications"]
#                 if pd["name"] == "Content"
#             ][0]

#             for key in TABLE_PRODUCT:
#                 prod_key = TABLE_PRODUCT[key]

#                 if prod.get(prod_key):
#                     prod_value = prod[prod_key]
#                     prod_db_row[key] = [prod_value]

#                 if prod_detail.get(prod_key):
#                     prod_value = prod_detail[prod_key]
#                     prod_db_row[key] = [prod_value]

#                 for prod_detail_att in prod_detail_atts:
#                     if prod_detail_att["code"] == prod_key:
#                         prod_db_row[key] = [prod_detail_att["value"]]

#                 if prod_db_row.get(key) is None:
#                     prod_db_row[key] = "N/A"

#             df_prod_db_row = pd.DataFrame(prod_db_row)
#             df_products = pd.concat([df_products, df_prod_db_row], ignore_index=True)

#             prod_childs = prod_detail["configurable_products"]
#             prod_child_db_row = {}

#             for prod_child in prod_childs:
#                 prod_child_id = prod_child["id"]

#                 # Product detail
#                 print(f"Crawling Product Child: {prod_child_id}")
#                 prod_child_driver, prod_child_soup = create_driver(
#                     URL_PRODUCT_CHILD_BY_SELLER.format(prod_child_id)
#                 )

#                 prod_child_data = pre_tag_to_json(prod_child_soup)
#                 prod_child_by_sellers = prod_child_data["all_sellers"]

#                 for pd_by_seller in prod_child_by_sellers:
#                     prod_child_db_row["id"] = [prod_child_id]
#                     prod_child_db_row["product_id"] = [prod_id]
#                     prod_child_db_row["color"] = [prod_child["option1"]]
#                     prod_child_db_row["seller_id"] = [pd_by_seller["seller"]["id"]]
#                     prod_child_db_row["store_id"] = [pd_by_seller["seller"]["store_id"]]
#                     prod_child_db_row["price"] = [pd_by_seller["price"]["value"]]

#                     df_prod_child_db_row = pd.DataFrame(prod_child_db_row)
#                     df_product_details = pd.concat(
#                         [df_product_details, df_prod_child_db_row], ignore_index=True
#                     )

#                 # Product review

#         except Exception as e:
#             print(e)
#             continue


# create_csv_file("products.csv", df_products)
# create_csv_file("product_details.csv", df_product_details)
create_csv_file("reviews.csv", df_reviews)
