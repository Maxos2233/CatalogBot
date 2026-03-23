from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client["warehouse"]
products = db["products"]

products.insert_one({
    "name": "Тест",
    "article": "Хуй",
    "quantity": 1
})

product = products.find_one({"article": "Хуй"})
print(product)