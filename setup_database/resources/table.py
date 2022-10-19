sql_brands = """
    CREATE TABLE IF NOT EXISTS brands (
        id INT,
        name VARCHAR(255) NOT NULL
    )
    """

sql_products = """
    CREATE TABLE IF NOT EXISTS products (
        id INT,
        brand_id INT,
        brand_name VARCHAR(255),
        nane VARCHAR(255),
        model VARCHAR(255),
        url_key VARCHAR(255),
        price INT,
        quantity_sold INT,
        create_at INT,
        battery_capacity VARCHAR(255),
        battery_type VARCHAR(255),
        bluetooth VARCHAR(255),
        camera_back VARCHAR(255),
        camera_front VARCHAR(255),
        camera_feature VARCHAR(255),
        card_slot VARCHAR(255),
        card_type VARCHAR(255),
        card_up_to VARCHAR(255),
        chipset VARCHAR(255),
        cpu VARCHAR(255),
        gpu VARCHAR(255),
        ram VARCHAR(255),
        storage_capacity VARCHAR(255),
        storage_capacity2 VARCHAR(255),
        dimensions VARCHAR(255),
        height VARCHAR(255),
        width VARCHAR(255),
        deep VARCHAR(255),
        weight VARCHAR(255),
        display_size VARCHAR(255),
        display_type VARCHAR(255),
        display_resolution VARCHAR(255),
        network_4g VARCHAR(255),
        accessories VARCHAR(255),
        headphone_jack VARCHAR(255),
        sim_slot VARCHAR(255),
        sim_type VARCHAR(255),
        material VARCHAR(255),
        charge_port VARCHAR(255),
        recording VARCHAR(255),
        wifi VARCHAR(255),
        made_in VARCHAR(255)
    )
"""

sql_product_details = """
    CREATE TABLE IF NOT EXISTS product_details (
        id INT,
        product_id INT,
        color VARCHAR(255),
        store_id INT,
        seller_id INT,
        price INT
    )
"""

sql_product_reviews = """
    CREATE TABLE IF NOT EXISTS product_reviews (
        product_id INT,
        child_id INT,
        seller_id INT,
        rating_1 INT,
        rating_2 INT,
        rating_3 INT,
        rating_4 INT,
        rating_5 INT
    )
"""

sql_sellers = """
    CREATE TABLE IF NOT EXISTS sellers (
        id INT,
        name VARCHAR(255)
    )
"""

sql_colors = """
    CREATE TABLE IF NOT EXISTS colors (
        id INT,
        name VARCHAR(255)
    )
"""

sql_locations = """
    CREATE TABLE IF NOT EXISTS locations (
        id VARCHAR(255),
        name VARCHAR(255)
    )
"""
