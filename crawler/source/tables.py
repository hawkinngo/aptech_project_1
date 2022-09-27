TABLE_LOCALTION = {"id": "query_value", "name": "display_value"}
TABLE_LOCALTION_COLUMNS = [key for key in TABLE_LOCALTION]

TABLE_BRAND = {
    "id": "query_value",
    "name": "display_value",
}
TABLE_BRAND_COLUMNS = [key for key in TABLE_BRAND]

TABLE_PRODUCT = {
    "id": "id",
    "brand_id": "brand_id",
    "brand_name": "brand_name",
    "name": "name",
    "model": "item_model_number",
    "url_key": "url_key",
    "price": "original_price",
    # "quantity_store": "quantity_store",
    "quantity_sold": "all_time_quantity_sold",
    "create_at": "day_ago_created",
    "battery_capacity": "battery_capacity",
    "battery_type": "loai_pin",
    "bluetooth": "bluetooth",
    "camera_back": "camera_back",
    "camera_front": "camera_front",
    "camera_feature": "tinh_nang_camera",
    "card_slot": "cart_slot",
    "card_type": "card_type",
    "card_up_to": "the_ngoai_toi_da",
    "chipset": "chip_set",
    "cpu": "cpu_speed",
    "gpu": "chip_do_hoa",
    "ram": "ram",
    "storage_capacity": "rom",
    "storage_capacity2": "kha_dung",
    "dimensions": "dimensions",
    "height": "height",
    "width": "width",
    "deep": "deep",
    "weight": "product_weight",
    "display_size": "screen_size",
    "display_type": "display_type",
    "display_resolution": "resolution",
    "network_4g": "ho_tro_4g",
    "accessories": "included_accessories",
    "headphone_jack": "jack_headphone",
    "sim_slot": "khe_sim",
    "sim_type": "loai_sim",
    "material": "material",
    "charge_port": "port_sac",
    "recording": "quay_phim",
    "wifi": "wifi",
    "made_in": "origin",
}
TABLE_PRODUCT_COLUMNS = [key for key in TABLE_PRODUCT]

TABLE_PRODUCT_DETAIL = {
    "id": "id",
    "product_id": "product_id",
    "color": "option1",
    "store_id": "store_id",
    "seller_id": "id",
    "price": "value",
}
TABLE_PRODUCT_DETAIL_COLUMNS = [key for key in TABLE_PRODUCT_DETAIL]

TABLE_REVIEW = {
    "product_id": "product_id",
    "child_id": "child_id",
    "seller_id": "seller_id",
    "rating_1": "1",
    "rating_2": "2",
    "rating_3": "3",
    "rating_4": "4",
    "rating_5": "5",
}

TABLE_REVIEW_COLUMNS = [key for key in TABLE_REVIEW]

BRANDS = {
    "id": "brand_id",
    "name": "brand_name",
}
BRANDS_COLUMNS = [key for key in BRANDS]

PRODUCTS = {
    "id": "id",
    "brand_id": "brand_id",
    "brand_name": "brand_name",
    "name": "name",
    "model": "item_model_number",
    "url_key": "url_key",
    "price": "original_price",
    # "quantity_store": "quantity_store",
    "quantity_sold": "all_time_quantity_sold",
    "create_at": "day_ago_created",
    "battery_capacity": "battery_capacity",
    "battery_type": "loai_pin",
    "bluetooth": "bluetooth",
    "camera_back": "camera_back",
    "camera_front": "camera_front",
    "camera_feature": "tinh_nang_camera",
    "card_slot": "cart_slot",
    "card_type": "card_type",
    "card_up_to": "the_ngoai_toi_da",
    "chipset": "chip_set",
    "cpu": "cpu_speed",
    "gpu": "chip_do_hoa",
    "ram": "ram",
    "storage_capacity": "rom",
    "storage_capacity2": "kha_dung",
    "dimensions": "dimensions",
    "height": "height",
    "width": "width",
    "deep": "deep",
    "weight": "product_weight",
    "display_size": "screen_size",
    "display_type": "display_type",
    "display_resolution": "resolution",
    "network_4g": "ho_tro_4g",
    "accessories": "included_accessories",
    "headphone_jack": "jack_headphone",
    "sim_slot": "khe_sim",
    "sim_type": "loai_sim",
    "material": "material",
    "charge_port": "port_sac",
    "recording": "quay_phim",
    "wifi": "wifi",
    "made_in": "origin",
}
PRODUCTS_COLUMNS = [key for key in PRODUCTS]

PRODUCT_DETAILS = {
    "id": "id",
    "product_id": "product_id",
    "seller_id": "seller_id",
    "color_name": "color_name",
    "url_key": "url_key",
    "sell_price": "sell_price",
    "rating": "rating",
}
PRODUCT_DETAILS_COLUMNS = [key for key in PRODUCT_DETAILS]

SELLERS = {
    "id": "id",
    "name": "name",
}
SELLERS_COLUMNS = [key for key in SELLERS]
