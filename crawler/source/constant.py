URL_PRODUCT = "https://tiki.vn/api/v2/products"
URL_PRODUCT_PAGES = URL_PRODUCT + "?limit=100&q=smartphone&category=1795&page={}"
URL_PRODUCT_DETAIL = URL_PRODUCT + "/{}"

URL_SELLER = "https://tiki.vn/api/v2/pdp/delivery/sellers/{}"
URL_REVIEW = "https://tiki.vn/api/v2/reviews?limit=20&include=comments,contribute_info&page={}&product_id={}&spid={}&seller_id={}"
PARAMS_PRODUCTS = "limit=100&q=smartphone&category=1795"
LAST_PAGE = ["paging", "last_page"]

FILE_BRAND_NAME = "brands.csv"
FILE_SELLER_NAME = "sellers.csv"
FILE_PRODUCT_NAME = "products.csv"
FILE_PRODUCT_DETAIL_NAME = "product_details.csv"

# PRODUCT_LIST = {
#     "URL": "https://tiki.vn/api/v2/products",
#     "PARAMS": {
#         "q": "smartphone",
#         "category": 1795,
#         "limit": 100,
#     },
#     "LAST_PAGE": ["paging", "last_page"],
# }

# PRODUCT_DETAIL = {
#     ATTRIBUTE: [
#         "id",
#         "name",
#         "seller_id",
#         "brand_id",
#         "url_path",
#         "price",
#         "discount",
#         "discount_rate",
#         "rating_average",
#         "review_count",
#         "inventory_status",
#         "inventory_quantity",
#         "quantity_sold",
#     ],
#     PRODUCT_SUB_DETAIL: ["id", "spid", "color", "price", "original_price"],
# }


# Seller
# https://tiki.vn/api/v2/pdp/delivery/sellers/146266085

# Rating
# https://tiki.vn/api/v2/reviews?limit=5&include=comments,contribute_info&sort=score%7Cdesc,id%7Cdesc,stars%7Call&page=1&spid=140614066&product_id=132068858&seller_id=213861
