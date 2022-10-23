.PHONY: db raw clean detail review

all: raw clean detail review db

db:
	cd setup_database && py main.py

clean:
	cd crawler && py crawl_product_clean.py

detail:
	cd crawler && py crawl_product_detail.py

review:
	cd crawler && py crawl_product_review.py

raw:
	cd crawler && py crawl_product_raw.py

test:
	cd crawler && py test.py