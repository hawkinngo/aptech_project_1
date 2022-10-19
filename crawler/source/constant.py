URL_PRODUCT = "https://tiki.vn/api/v2/products"
URL_PRODUCT_LIST = "https://tiki.vn/api/personalish/v1/blocks/listings?limit=300&aggregations=2&category=1795"
URL_PRODUCT_BY_BRAND = "https://tiki.vn/api/v2/products?limit=100&aggregations=2&brand={}&category=1795&page={}"
# URL_PRODUCT_LIST = URL_PRODUCT + "?limit=100&q=smartphone&category=1795&aggregations=2"

URL_PRODUCT_PAGE = URL_PRODUCT + "?limit=100&q=smartphone&category=1795&page={}"
URL_PRODUCT_BY_SELLER = "https://api.tiki.vn/seller-store/v2/collections/5/products?seller_id={}&limit=100&cursor=0&category=1795&urlKey=dien-thoai-smartphone"
URL_PRODUCT_DETAIL = URL_PRODUCT + "/{}"
URL_PRODUCT_CHILD_BY_SELLER = "https://tiki.vn/api/v2/pdp/delivery/sellers/{}"

URL_SELLER = "https://tiki.vn/api/v2/pdp/delivery/sellers/{}"
URL_REVIEW = "https://tiki.vn/api/v2/reviews?limit=20&include=comments,contribute_info&page={}&product_id={}&seller_id={}"
PARAMS_PRODUCTS = "limit=100&q=smartphone&category=1795"

OUTSOURCE_PATH = "output/csv2/{}"
PRODUCTS_RAW_FILE = "products_raw.csv"
PRODUCTS_FILTER_FILE = "products_filters.csv"
PRODUCTS_DETAIL_LV1 = "products_detail_lv1.csv"
STORAGES_FILE = "storages.csv"
RAMS_FILE = "rams.csv"
COLORS_FILE = "colors.csv"

CLEANSOURCE_PATH = "output/clean/{}"
BRANDS_FILE = "brands.csv"
PRODUCTS_FILE = "products.csv"
PRODUCT_DETAILS_FILE = "product_details.csv"
SELLERS_FILE = "sellers.csv"
REVIEWS_FILE = "product_reviews.csv"

FILTER_GENUINE_LIST_BASE = ["Hàng Chính hãng", "HàNg ChíNh HãNg"]
FILTER_USED_LIST_BASE = [
    "đã kích hoạt bảo hành điện tử",
    "đã kích hoạt điện tử",
    "đã kích hoạt bảo hành",
    "chưa active",
]
FILTER_ANY_TEXT_BASE = [
    "Kg5K",
    "Kf6P",
    "HàNg ChíNh HãNg",
    "Hàng Chính Hãng",
    "(4+2)GB",
    "smartphone",
    "điện thoại",
    "điiện thoại",
    "di động",
    "Android 11",
    "quốc tế",
    "hàng nhập khẩu",
    "hàng đầu",
    "thông minh",
    "chiến game",
    "cực đỉnh",
    "Màn hình",
    "độ phân giải",
    "IPS",
    "MH",
    "AMOLED",
    "FHD",
    "Full",
    "HD+",
    "165Hz",
    "120Hz",
    "90Hz",
    "6.67",
    "6.8",
    "6.7",
    "6.6",
    "6.5",
    "6,39",
    "5.7",
    '"',
    "mới",
    "inch",
    "đục lỗ",
    "đục lổ",
    "tùy biến mở rộng tới 7GB",
    "Mở khóa",
    "khuôn mặt + vân tay",
    "khuôn mặt",
    "vân tay",
    "Mở khoá bằng Gương Mặt",
    "Pin",
    "21000",
    "10.600",
    "10.000",
    "8.000",
    "7000",
    "6000",
    "5050",
    "5000",
    "5.000",
    "4200",
    "4000",
    "mAh",
    "Gaming",
    "Chơi Game",
    "Chuyên Game",
    "chơi game cực đỉnh",
    "music" "Ngôn Ngữ",
    "Hỗ trợ Tiếng Việt",
    "có tiếng việt",
    "khủng",
    "thông minh",
    "nguyên seal",
    "full ngôn ngữ",
    "Ngôn Ngữ",
    "bảo mật",
    "Pre Order",
    "Camera",
    "Máy ảnh",
    "nhiếp ảnh điện toán",
    "108MP",
    "64MP",
    "48MP",
    "20MP",
    "13MP",
    "Triple Al",
    "Lte" "MH",
    "giọt nước",
    "Tầm nhìn",
    "nhìn",
    "ban đêm",
    "BH 12 tháng",
    "Sạc nhanh",
    "/Sạc",
    "67W",
    "66W",
    "33W",
    "30W",
    "22.5W",
    "18W",
    "Chip Octa 1.6GHz",
    "Snapdragon 888",
    "Snapdragon 870",
    "Snapdragon 695G",
    "Snapdragon 695",
    "Snapdragon 680",
    "Snapdragon 653",
    "653",
    "/SNAP695",
    "MediaTek Dimensity 8100",
    "Qualcomm Snapdragon 8 Gen 1",
    "MediaTek",
    "G99",
    "G96",
    "MediaTek G99",
    "8 nhân",
    "HT làm mát 8.0",
    "Helio",
    "G95",
    "G88",
    "G35",
    "G25",
    "/108+8+2MP/16MP/",
    "LTE",
    "Dimensity 810",
    "Music",
    "RAM",
    "ROM",
    "2 sim",
    "hai SIM",
    "kép",
    "Bộ nhớ mở rộng",
    "Bộ ba",
    "2 sóng",
    "chống sốc",
    "chống va đập",
    "chống nước",
    "IP68",
    "in",
    "NFC..",
    " l ",
    "ZTE 8045",
]
FILTER_SPECIAL_LIST_BASE = [
    "(",
    ")",
    "-",
    "|",
    "–",
    "[",
    "]",
    ",",
    # "+"
]


def full_case_text(text_list):
    full_case = []

    for atext in text_list:
        full_case.append(atext)
        full_case.append(atext.lower())
        full_case.append(atext.capitalize())
        full_case.append(atext.title())
        full_case.append(atext.upper())

    return full_case


FILTER_GENUINE_LIST = full_case_text(FILTER_GENUINE_LIST_BASE)
FILTER_USED_LIST = full_case_text(FILTER_USED_LIST_BASE)
FILTER_ANY_TEXT = full_case_text(FILTER_ANY_TEXT_BASE)

FILTER_LIST = (
    FILTER_GENUINE_LIST + FILTER_USED_LIST + FILTER_ANY_TEXT + FILTER_SPECIAL_LIST_BASE
)

REPLACE_PRODUCT_NAME = {
    "//": "",
    "//12": "",
    "Kg5K": "",
    " Fe ": " FE ",
    " Se ": " SE ",
    "Flip 4": "Flip4",
    "Flip 3": "Flip3",
    "Fold 4": "Fold4",
    "Fold 3": "Fold3",
    "Joy 4": "Joy4",
    "Zte": "ZTE",
    "/ ": "",
    " + ": "/",
    "Gb": "GB",
    "3GB/32G ": "3GB/32GB",
    "3/32": "3GB/32GB",
    "2/32GB": "2GB/32GB",
    "332GB": "3GB/32GB",
    "3GB/32G": "3GB/32GB",
    "2GB/32 GB": "3GB/32GB",
    "3+32GB": "3GB/32GB",
    "4GB 32GB": "4GB/32GB",
    "3/64": "3GB/64GB",
    "4G+64G ": "4GB/64GB",
    "4GB 64GB": "4GB/64GB",
    "4GB/64G": "4GB/64GB",
    "4/128GB": "4GB/128GB",
    "4+128GB": "4GB/128GB",
    "128GB 6GB": "6GB/128GB",
    "6+128GB": "6GB/128GB",
    "6+5GB/128GB": "6GB/128GB",
    "8+5GB/128GB": "8GB/128GB 5GB/128GB",
    "6+128GB/8+256GB": "6GB/128GB 8GB/256GB",
    "6GB+128GB /8GB+256GB": "6GB/128GB 8GB/256GB",
    "6GB 128GB": "6GB/128GB",
    "6GB 128 GB": "6GB/128GB",
    "6+128GB/8+256GB": "6GB/128GB 8GB/256GB",
    "8+128GB/8+256GB": "8GB/128GB 8GB/256GB",
    "8G/128GB": "8GB/128GB",
    "8/128GB": "8GB/128GB",
    "8/256GB": "8GB/256GB",
    "8GB128GB": "8GB/128GB",
    "8GB/128G ": "8GB/128GB",
    "8GB 128GB": "8GB/128GB",
    "8GB/128G": "8GB/128GB",
    "8GB/256G": "8GB/256GB",
    "8G 256G": "8GB/256GB",
    "5G/8G/256G": "8GB/256GB",
    "12/256GB": "12GB/256GB",
    "12+128GB/16+256GB": "12GB/128GB 16GB/256GB",
    "4GB+3GB/64GB": "4GB/64GB 3GB/64GB",
    "2GB+32GB/3GB+64GB": "2GB/32GB 3GB/64GB",
    "4GB+64GB/6GB+128GB": "4GB/64GB 6GB/128GB",
    "4GB/6GB/128GB/128GB": "4GB/64GB 6GB/128GB",
    "6GB/128GB/8+256GB": "6GB/128GB 8GB/256GB",
    "6GB/128G": "6GB/128GB",
    "3GB/32GBB": "3GB/32GB",
    "4GB/64GBB": "4GB/64GB",
    "4GB/128GBB": "4GB/128GB",
    "6GB/128GBB": "6GB/128GB",
    "8GB/128GBB": "8GB/128GB",
    "8GB/256GBB": "8GB/256GB",
}

FILTER_CLEAN = [
    "2GB/16GB",
    "2GB/32GB",
    "2GB/64GB",
    "3GB/32GB",
    "3GB/64GB",
    "4GB/32GB",
    "4GB/64GB",
    "4GB/128GB",
    "5GB/128GB",
    "6GB/128GB",
    "8GB/128GB",
    "8GB/256GB",
    "12GB/256GB",
    "12GB/128GB",
    "16GB/256GB",
    "12GB/512GB",
    "512GB",
    "256GB",
    "128GB",
    "64GB",
    "32GB",
    "8GB",
    "4GB",
]

# color options
COLOR_FILTER_SILVER = ["Chrome Silver"]
COLOR_FILTER_GREY = ["Grey", "Graphite Gray"]
COLOR_FILTER_BLUE = [
    "Xanh Ánh Sao",
    "Xanh Hoàng Hôn",
    "Blue",
    "Xanh Đại Tây Dương",
    "Xanh Ánh Sao",
    "Xanh Chạng Vạng",
    "Xanh Lam",
    "Ocen Blue",
    "Xanh Biển",
    "Sky Blue",
]
COLOR_FILTER_WHITE = ["White"]
COLOR_FILTER_BLACK = ["Black"]
