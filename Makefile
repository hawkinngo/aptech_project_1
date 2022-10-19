addition:
	cd crawler && py crawl_product_clean.py

product_detail:
	cd crawler && py crawl_product_detail.py

product_review:
	cd crawler && py crawl_product_review.py

raw:
	cd crawler && py crawl_product_raw.py

crawl_product:
	cd crawler && py crawl_product.py

crawl_review:
	cd crawler && py crawl_review_new.py

db:
	cd setup_database && py main.py