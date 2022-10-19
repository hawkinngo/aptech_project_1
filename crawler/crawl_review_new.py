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
    df_read_csv,
)

from source.tables import (
    TABLE_PRODUCT,
    TABLE_PRODUCT_COLUMNS,
    TABLE_PRODUCT_DETAIL,
    TABLE_PRODUCT_DETAIL_COLUMNS,
    TABLE_REVIEW,
    TABLE_REVIEW_COLUMNS,
)

product_crawled = 418

products_csv = "output/csv/products_new.csv"
sellers_csv = "output/csv/sellers.csv"
reviews_csv = "output/csv/product_reviews.csv"

products = pd.read_csv(products_csv).to_dict("records")[product_crawled:]
sellers = pd.read_csv(sellers_csv).to_dict("records")
reviews = pd.read_csv(reviews_csv).to_dict("records")

df_reviews = df_read_csv(reviews_csv)
# df_reviews = pd.read_csv(reviews_csv)
# first_column = df_reviews.columns[0]
# df_reviews = df_reviews.drop([first_column], axis=1)

json_dump(products[0])
print(len(products))
