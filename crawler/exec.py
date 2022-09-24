import json

from source.driver import create_driver, product_crawl
from source.constant import (
    URL_PRODUCT_PAGES,
    URL_PRODUCT_DETAIL,
    URL_SELLER,
    URL_REVIEW,
)
from source.utils import pre_tag_to_json, get_last_page, create_json_file, json_dump

# Define Empty List
total_products = []
total_product_details = []
total_product_sellers = []
total_reviews = []

# Get Total Products
url_product_page = URL_PRODUCT_PAGES.format(1)
print(f"Crawling Product Pages: {url_product_page}")
driver_product_page, product_pages_soup = create_driver(url_product_page)

product_pages_json = pre_tag_to_json(product_pages_soup)
total_products += product_pages_json["data"]

product_last_page = get_last_page(product_pages_json) + 1

for page in range(2, product_last_page):
    url_product_page = URL_PRODUCT_PAGES.format(page)
    print(f"Crawling Product Pages: {url_product_page}")

    driver_product_page, product_pages_soup = create_driver(url_product_page)
    product_pages_json = pre_tag_to_json(product_pages_soup)

    total_products += product_pages_json["data"]

create_json_file("products.json", total_products)


# Get Product Details
for product in total_products:
    product_id = product["id"]
    url_product_detail = URL_PRODUCT_DETAIL.format(product_id)

    print(f"Crawling Product Detail: {url_product_detail}")
    driver_product_detail, product_detail_soup = create_driver(url_product_detail)
    product_detail_json = pre_tag_to_json(product_detail_soup)

    total_product_details.append(product_detail_json)

create_json_file("product_details.json", total_product_details)

# Get Sellers
for product_detail in total_product_details:
    try:
        product_id = product_detail["id"]

        configurable_products = product_detail["configurable_products"]
        for cp in configurable_products:
            cp_id = cp["id"]
            url_seller = URL_SELLER.format(cp_id)
            print(f"Crawling Sellers: {url_seller}")

            driver_product_sellers, product_sellers_soup = create_driver(url_seller)
            product_sellers = pre_tag_to_json(product_sellers_soup)["all_sellers"]

            total_product_sellers += product_sellers

            for product_seller in product_sellers:
                seller_id = product_seller["seller"]["id"]
                url_review = URL_REVIEW.format(1, product_id, cp_id, seller_id)
                print(f"Crawling Reviews: {url_review}")
                driver_reviews, reviews_soup = create_driver(url_review)
                reviews_json = pre_tag_to_json(reviews_soup)
                total_reviews += reviews_json["data"]
                review_last_page = get_last_page(reviews_json) + 1

                if review_last_page > 2:
                    for page in range(2, review_last_page):
                        url_review = URL_REVIEW.format(
                            page, product_id, cp_id, seller_id
                        )
                        print(f"Crawling Reviews: {url_review}")
                        driver_reviews, reviews_soup = create_driver(url_review)
                        reviews_json = pre_tag_to_json(reviews_soup)

                        total_reviews += reviews_json["data"]

    except Exception as exp:
        print(f"Error {exp}")
        continue

create_json_file("product_sellers.json", total_product_sellers)
create_json_file("reviews.json", total_reviews)
