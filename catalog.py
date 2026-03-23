import database

def add_product(name, article, quantity):
    product_info = {"name": name, "article": article, "quantity": quantity}
    database.products.insert_one(product_info)
    return "Товар добавлен в каталог"

def load_catalog():
    catalog = []
    try:
        catalog = database.products.find()
    except FileNotFoundError:
        pass
    return catalog

def delete_product(article):
    catalog = database.products.find()
    new_catalog = []
    product_exist = any(product["article"] == article for product in catalog)
    for product in catalog:
        if article != product["article"]:
            new_catalog.append(product)
    if not product_exist:
        return "Такого товара нет"
    database.products.delete_one({"article": article})
    return "Товар удален"

def show_product():
    catalog = database.products.find()
    result = ""
    for product in catalog:
        result += f"{product['name']} - {product['article']} - {product['quantity']}\n\n"
    return result

def edit_product(article, quantity):
    catalog = database.products.find()
    for product in catalog:
        if article == product["article"]:
            product["quantity"] = quantity
    database.products.update_one({"article": article}, {"$set": {"quantity": quantity}})
    return f"Для товара {article}, было задано новое количество - {quantity}"

def search_product(article):
    catalog = database.products.find()
    result = ""
    for product in catalog:
        if article == product["article"] :
            result += f"{product['name']} - {product['article']} - {product['quantity']}"
            return result
    return "Товар не найден"

def product_exists(article):
    catalog = database.products.find()
    product_exist = any(product["article"] == article for product in catalog)
    if not product_exist:
        return None
    return True