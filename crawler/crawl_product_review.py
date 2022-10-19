import json
import pandas as pd
import csv
from pprint import pprint

from source.driver import create_driver_request

from source.constant import (
    OUTSOURCE_PATH,
    CLEANSOURCE_PATH,
    PRODUCTS_FILTER_FILE,
    SELLERS_FILE,
    REVIEWS_FILE,
    URL_REVIEW,
)

from source.utils import df_read_csv, create_csv_file

products_raw_csv = OUTSOURCE_PATH.format(PRODUCTS_FILTER_FILE)
df_products_raw = df_read_csv(products_raw_csv)
products_raw = df_products_raw.to_dict("records")

sellers_csv = OUTSOURCE_PATH.format(SELLERS_FILE)
df_sellers = df_read_csv(sellers_csv)
sellers = df_sellers.to_dict("records")

reviews_csv = OUTSOURCE_PATH.format(REVIEWS_FILE)
# df_reviews = df_read_csv(reviews_csv)

# reviews_csv = OUTSOURCE_PATH.format("test_reviews.csv")
df_reviews = (
    df_read_csv(reviews_csv)
    if df_read_csv(reviews_csv) is not False
    else pd.DataFrame(
        columns=[
            "product_id",
            "product_detail_id",
            "seller_id",
            "rating_1",
            "rating_2",
            "rating_3",
            "rating_4",
            "rating_5",
        ]
    )
)

reviews_list = df_reviews.to_dict("records")

index_must_pass = -1

for product_index, product in enumerate(products_raw):

    if product_index <= index_must_pass:
        continue

    product_id = product["id"]

    for seller in sellers:
        seller_id = seller["id"]

        get_reviews = create_driver_request(URL_REVIEW.format(1, product_id, seller_id))

        total_reviews = get_reviews["paging"]["total"]
        total_page = get_reviews["paging"]["last_page"] + 1

        if total_reviews == 0:
            print(
                f"Product {product_index} --- {product_id} and Seller {seller_id} has no review"
            )
            pass

        review_row = {}
        count_reviews = {}

        for i in range(1, total_page):
            reviews = create_driver_request(
                URL_REVIEW.format(i, product_id, seller_id)
            )["data"]

            print(
                f"Crawling {product_index} --- product_id {product_id} seller_id {seller_id} - page {i}"
            )

            for review in reviews:

                product_detail_id = review["spid"]
                rating = review["rating"]

                if count_reviews.get(product_detail_id) is None:
                    count_reviews[product_detail_id] = {
                        "rating_1": 0,
                        "rating_2": 0,
                        "rating_3": 0,
                        "rating_4": 0,
                        "rating_5": 0,
                    }

                if rating == 1:
                    count_reviews[product_detail_id]["rating_1"] += 1
                if rating == 2:
                    count_reviews[product_detail_id]["rating_2"] += 1
                if rating == 3:
                    count_reviews[product_detail_id]["rating_3"] += 1
                if rating == 4:
                    count_reviews[product_detail_id]["rating_4"] += 1
                if rating == 5:
                    count_reviews[product_detail_id]["rating_5"] += 1

        # print("count reviews:", count_reviews)

        for key in count_reviews:
            count_review = count_reviews[key]
            review_row["product_id"] = [product_id]
            review_row["product_detail_id"] = [key]
            review_row["seller_id"] = [seller_id]
            review_row["rating_1"] = [count_review["rating_1"]]
            review_row["rating_2"] = [count_review["rating_2"]]
            review_row["rating_3"] = [count_review["rating_3"]]
            review_row["rating_4"] = [count_review["rating_4"]]
            review_row["rating_5"] = [count_review["rating_5"]]

            df_review_row = pd.DataFrame(review_row)
            check_exists_count_review = len(
                df_reviews[
                    (df_reviews["seller_id"] == seller_id)
                    & (df_reviews["product_detail_id"] == key)
                    & (df_reviews["product_id"] == product_id)
                ]
            )

            if check_exists_count_review == 0:
                df_reviews = pd.concat([df_reviews, df_review_row], ignore_index=True)

    print(df_reviews)
    create_csv_file(REVIEWS_FILE, df_reviews)
