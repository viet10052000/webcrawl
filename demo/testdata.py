import pymongo

# Kết nối tới MongoDB
client = pymongo.MongoClient('mongodb+srv://user:123456Aa@cluster0.t3aqomt.mongodb.net')
db = client['shops']
collection = db['products']
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

def preprocess_text(text):
    # Thực hiện các bước tiền xử lý văn bản (loại bỏ dấu, chuyển thành chữ thường, ...)
    # Có thể sử dụng các công cụ như nltk, unidecode, regex, ...
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    tokens = word_tokenize(text.lower())
    filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalpha() and token not in stop_words]
    processed_text = " ".join(filtered_tokens)

    return processed_text

def group_similar_products(products):
    # Chuẩn hóa và tạo ma trận đặc trưng TF-IDF cho tên sản phẩm
    product_names = [product.name for product in products]
    normalized_names = [preprocess_text(name.lower()) for name in product_names]
    vectorizer = TfidfVectorizer()
    name_features = vectorizer.fit_transform(normalized_names)

    # Gom nhóm các sản phẩm dựa trên tên
    num_clusters = 3  # Số lượng nhóm cần gom
    clustering = KMeans(n_clusters=num_clusters, n_init=10)
    name_clusters = clustering.fit_predict(name_features)

    # Chuẩn hóa và tạo ma trận đặc trưng cho giá sản phẩm
    product_prices = [product.price for product in products]
    price_features = numpy.array(product_prices).reshape(-1, 1)

    # Gom nhóm các sản phẩm dựa trên giá
    clustering = KMeans(n_clusters=num_clusters, n_init=10)
    price_clusters = clustering.fit_predict(price_features)

    # Kết hợp các nhóm từ cả tên và giá
    combined_clusters = [f"{name_cluster}-{price_cluster}" for name_cluster, price_cluster in zip(name_clusters, price_clusters)]

    # Gán nhóm cho từng sản phẩm
    for i, product in enumerate(products):
        product.cluster = combined_clusters[i]

    return products

def compare_prices(product1, product2):
    return abs(product1.price - product2.price)

def find_similar_products(target_product, products):
    similar_products = []
    target_cluster = target_product.cluster

    for product in products:
        if product.cluster == target_cluster and product != target_product:
            similar_products.append(product)

    return similar_products

# Dữ liệu mẫu về sản phẩm và giá
product_data = [
    ("iPhone 12 Pro", 1000),
    ("iPhone 12 Mini", 700),
    ("Samsung Galaxy S21", 900),
    ("Samsung Galaxy S20", 800),
    ("Google Pixel 5", 800),
    ("Google Pixel 4a", 400),
    ("OnePlus 9 Pro", 950),
    ("OnePlus 8T", 850),
]

# Tạo danh sách sản phẩm từ dữ liệu mẫu
products = [Product(name, price) for name, price in product_data]

# Gom nhóm các sản phẩm tương đồng
grouped_products = group_similar_products(products)

# So sánh giá sản phẩm
target_product = grouped_products[0]
similar_products = find_similar_products(target_product, grouped_products)
similar_products.sort(key=lambda x: compare_prices(target_product, x))

# In kết quả
print("Target Product:")
print(f"Name: {target_product.name}, Price: {target_product.price}\n")

print("Similar Products:")
for product in similar_products:
    print(f"Name: {product.name}, Price: {product.price}")