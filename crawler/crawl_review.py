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
reviews_csv = "output/csv/product_reviews.csv"

products = pd.read_csv(products_csv).to_dict("records")
sellers = pd.read_csv(sellers_csv).to_dict("records")
reviews = pd.read_csv(reviews_csv).to_dict("records")

df_reviews = pd.read_csv(reviews_csv)
first_column = df_reviews.columns[0]
df_reviews = df_reviews.drop([first_column], axis=1)

for prod_index, product in enumerate(products):
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
                    f"Crawling {prod_index} --- product_id {prod_id} seller_id {seller_id} - page {review_page}"
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

        else:
            print(
                f"Product {prod_index} --- {prod_id} and Seller {seller_id} has no review"
            )

    create_csv_file("product_reviews.csv", df_reviews)
