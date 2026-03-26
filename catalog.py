import database
from models import ProductCreateDTO, ProductUpdateDTO, ProductShowDTO, ProductGetArticleDTO, ProductEntity


def add_product(dto: ProductCreateDTO):
    entity = ProductEntity(
        name=dto.name,
        article=dto.article,
        quantity=dto.quantity,
    )
    database.products.insert_one({
        "name": entity.name,
        "article": entity.article,
        "quantity": entity.quantity,
    })
    return "Товар добавлен в каталог"

def load_catalog():
    catalog = []
    try:
        catalog = database.products.find()
    except FileNotFoundError:
        pass
    return catalog

def delete_product(dto: ProductGetArticleDTO):
    database.products.delete_one({"article": dto.article})
    return "Товар удален"

def show_product():
    catalog = database.products.find()
    result = ""
    for product in catalog:
        entity = ProductEntity(
            name = product["name"],
            article = product["article"],
            quantity = product["quantity"]
        )
        result += f"{entity.name} - {entity.article} - {entity.quantity}\n\n"
    return result

def edit_product(dto: ProductUpdateDTO):
    database.products.update_one({"article": dto.article}, {"$set": {"quantity": dto.quantity}})
    return f"Для товара {dto.article}, было задано новое количество - {dto.quantity}"

def search_product(dto: ProductGetArticleDTO):
    catalog = database.products.find()
    result = ""
    for product in catalog:
        if dto.article == product["article"] :
            entity = ProductEntity(
                name = product["name"],
                article = product["article"],
                quantity = product["quantity"]
            )
            transform_to_dto = ProductShowDTO(
                name = entity.name,
                article = entity.article,
                quantity = entity.quantity
            )
            result += f"{transform_to_dto.name} - {transform_to_dto.article} - {transform_to_dto.quantity}\n\n"
            return result
    return "Товар не найден"

def product_exists(dto: ProductGetArticleDTO):
    catalog = database.products.find()
    product_exist = any(product["article"] == dto.article for product in catalog)
    return product_exist