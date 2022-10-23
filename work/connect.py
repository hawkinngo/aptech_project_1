import psycopg2 as pg2
import pandas as pd

# DB_HOST = "arjuna.db.elephantsql.com"
DB_HOST = "db.wzftgqxiaxiaknyscdjv.supabase.co"
DB_PORT = "5432"
# DB_NAME = "fgibkuls"
DB_NAME = "postgres"
# DB_USER = "fgibkuls"
DB_USER = "postgres"
# DB_PASS = "xOfEt9NcdAdsGmAQjLsQvC4F9wJC0Y9O"
DB_PASS = "aptechprojectdb"


connection = pg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)
cursor = connection.cursor()


def get_table(sql):
    cursor.execute(sql)
    data = cursor.fetchall()

    cols = []
    for brand in cursor.description:
        cols.append(brand[0])

    df = pd.DataFrame(data=data, columns=cols)
    return df


df_brands = get_table("""SELECT * FROM brands""")
df_products = get_table("""SELECT * FROM products""")
df_product_details = get_table("""SELECT * FROM product_details""")
df_reviews = get_table("""SELECT * FROM reviews""")
df_sellers = get_table("""SELECT * FROM sellers""")

merge_brand_product = (
    pd.merge(
        left=df_products,
        right=df_brands,
        how="left",
        left_on="brand_id",
        right_on="id",
    )
    .drop(["id_y", "brand_id"], axis=1)
    .rename(columns={"id_x": "id", "name_x": "name", "name_y": "brand_name"})
)
# print(merge_brand_product)


merge_product_detail = pd.merge(
    left=df_product_details,
    right=merge_brand_product,
    how="left",
    left_on="product_id",
    right_on="id",
).drop(["id"], axis=1)
# print(merge_product_detail)

merge_product_review = pd.merge(
    left=merge_product_detail,
    right=df_reviews,
    how="left",
    left_on=["product_detail_id", "seller"],
    right_on=["product_detail_id", "seller_id"],
).drop(
    ["id", "seller_id", "product_id_crawl", "product_detail_id", "product_id"], axis=1
)
print(merge_product_review)

merge_product_seller = (
    pd.merge(
        left=merge_product_review,
        right=df_sellers,
        left_on="seller",
        right_on="id",
    )
    .drop(["id", "seller", "address"], axis=1)
    .rename(columns={"name_y": "seller", "name_x": "name"})
    .reindex(
        columns=[
            "brand_name",
            "name",
            "seller",
            "color",
            "is_genuine",
            "is_used",
            "is_imported_goods",
            "ram",
            "storage_capacity",
            "original_price",
            "sell_price",
            "rating_1",
            "rating_2",
            "rating_3",
            "rating_4",
            "rating_5",
        ]
    )
)
# print(merge_product_seller)

database = merge_product_seller
