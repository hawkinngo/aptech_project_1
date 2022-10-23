import pandas as pd

from source.constant import (
    OUTSOURCE_PATH,
    CLEANSOURCE_PATH,
    BRANDS_FILE,
    PRODUCTS_FILE,
    PRODUCT_DETAILS_FILE,
    REVIEWS_FILE,
    SELLERS_FILE,
)

from source.utils import df_read_csv, create_csv_file

pd.set_option("display.max_columns", None)
# pd.set_option("display.max_rows", None)


def get_table(sql):
    cursor.execute(sql)
    data = cursor.fetchall()

    cols = []
    for brand in cursor.description:
        cols.append(brand[0])

    df = pd.DataFrame(data=data, columns=cols)
    return df


brands_csv = CLEANSOURCE_PATH.format(BRANDS_FILE)
df_brands = df_read_csv(brands_csv)

products_csv = CLEANSOURCE_PATH.format(PRODUCTS_FILE)
df_products = df_read_csv(products_csv)

product_details_csv = CLEANSOURCE_PATH.format(PRODUCT_DETAILS_FILE)
df_product_details = df_read_csv(product_details_csv)

reviews_csv = CLEANSOURCE_PATH.format(REVIEWS_FILE)
df_reviews = df_read_csv(reviews_csv)

sellers_csv = CLEANSOURCE_PATH.format(SELLERS_FILE)
df_sellers = df_read_csv(sellers_csv)

# df_brands = get_table("""SELECT * FROM brands""")
# df_products = get_table("""SELECT * FROM products""")
# df_product_details = get_table("""SELECT * FROM product_details""")
# df_reviews = get_table("""SELECT * FROM reviews""")
# df_sellers = get_table("""SELECT * FROM sellers""")

merge_brand_product = (
    pd.merge(
        left=df_products,
        right=df_brands,
        how="left",
        left_on="brand_id",
        right_on="id",
    )
    .drop(["brand_id"], axis=1)
    .rename(columns={"name_x": "name", "name_y": "brand_name"})
)

merge_brand_product.index += 1
merge_brand_product.reset_index(names=["product_id"], inplace=True)
# print("df_products\n", df_products)
# print("merge_brand_product\n", merge_brand_product)


merge_product_detail = pd.merge(
    left=df_product_details,
    right=merge_brand_product,
    how="left",
    left_on="product_id",
    right_on="product_id",
).drop(["id"], axis=1)
# print("df_product_details\n", df_product_details)
# print("merge_brand_product\n", merge_brand_product)
# print("merge_product_detail\n", merge_product_detail)

merge_product_review = pd.merge(
    left=merge_product_detail,
    right=df_reviews,
    how="left",
    left_on=["product_detail_id", "seller"],
    right_on=["product_detail_id", "seller_id"],
).drop(
    ["id", "seller_id", "product_id_crawl", "product_detail_id", "product_id"], axis=1
)

for i, mpr in merge_product_review.iterrows():
    merge_product_review.loc[i, "rating_1"] = (
        mpr["rating_1"] if mpr["rating_1"] >= 0 else 0
    )
    merge_product_review.loc[i, "rating_2"] = (
        mpr["rating_2"] if mpr["rating_2"] >= 0 else 0
    )
    merge_product_review.loc[i, "rating_3"] = (
        mpr["rating_3"] if mpr["rating_3"] >= 0 else 0
    )
    merge_product_review.loc[i, "rating_4"] = (
        mpr["rating_4"] if mpr["rating_4"] >= 0 else 0
    )
    merge_product_review.loc[i, "rating_5"] = (
        mpr["rating_5"] if mpr["rating_5"] >= 0 else 0
    )

# print("merge_product_detail\n", merge_product_detail)
# print("df_reviews\n", df_reviews)
# print("merge_product_review\n", merge_product_review)


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

# print("merge_product_review\n", merge_product_review)
# print("df_sellers\n", df_sellers)
# print("merge_product_seller\n", merge_product_seller)

create_csv_file("general.csv", merge_product_seller, is_clean=True)
