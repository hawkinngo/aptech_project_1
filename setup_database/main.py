import psycopg2
import pandas as pd
import sys
import numpy as np

from sqlalchemy import create_engine
from os import path
from os.path import dirname, abspath

root_dir = dirname(dirname(__file__))
crawler = path.join(root_dir, "crawler", "source")
sys.path.append(crawler)

from constant import (
    BRANDS_FILE,
    PRODUCTS_FILE,
    SELLERS_FILE,
    PRODUCT_DETAILS_FILE,
    REVIEWS_FILE,
    COLORS_FILE,
)

from resources.constant import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
from resources.utils import df_read_csv
from resources.table import (
    sql_brands,
    sql_products,
    sql_product_details,
    sql_product_reviews,
    sql_colors,
    sql_sellers,
    sql_locations,
)

conn_str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
db = create_engine(conn_str)
conn = db.connect()

# Upload to host
clean_dir = path.join(root_dir, "crawler\output\clean")

brands_csv = path.join(clean_dir, BRANDS_FILE)
df_brands = df_read_csv(brands_csv)
df_brands.to_sql("brands", con=conn, if_exists="replace", index=False)
print("brands table created")

sellers_csv = path.join(clean_dir, SELLERS_FILE)
df_sellers = df_read_csv(sellers_csv)
df_sellers.to_sql("sellers", con=conn, if_exists="replace", index=False)
print("sellers table created")

colors_csv = path.join(clean_dir, COLORS_FILE)
df_colors = df_read_csv(colors_csv)
df_colors.to_sql("colors", con=conn, if_exists="replace", index=False)
print("colors table created")

products_csv = path.join(clean_dir, PRODUCTS_FILE)
df_products = df_read_csv(products_csv)
df_products.index += 1
df_products.index.rename(name="id", inplace=True)
df_products.to_sql("products", con=conn, if_exists="replace", index=True)
print("products table created")

product_details_csv = path.join(clean_dir, PRODUCT_DETAILS_FILE)
df_product_details = df_read_csv(product_details_csv)
df_product_details.to_sql("product_details", con=conn, if_exists="replace", index=False)
print("product_details table created")

product_reviews_csv = path.join(clean_dir, REVIEWS_FILE)
df_product_reviews = df_read_csv(product_reviews_csv)
df_product_reviews.to_sql("reviews", con=conn, if_exists="replace", index=False)
print("reviews table created")
