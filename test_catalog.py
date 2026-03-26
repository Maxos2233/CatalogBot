from unittest.mock import MagicMock
import catalog
from models import ProductGetArticleDTO, ProductCreateDTO, ProductUpdateDTO, ProductShowDTO


def test_product_exists_returns_true():
    catalog.database.products.find = MagicMock(return_value=[{"article": "Пизда", "name": "манда", "quantity": 123}])

    dto = ProductGetArticleDTO(article="Пизда")
    result = catalog.product_exists(dto)
    assert result == True

def test_product_exists_returns_none():
    catalog.database.products.find = MagicMock(return_value=[{"article": "Пизда", "name": "манда", "quantity": 123}])

    dto = ProductGetArticleDTO(article="Рыготина")
    result = catalog.product_exists(dto)
    assert result == False

def test_delete_product_exist():
    catalog.database.products.delete_one = MagicMock(return_value=[{"article": "Пизда"}])
    dto = ProductGetArticleDTO(article="Пизда")
    result = catalog.delete_product(dto)
    assert result == "Товар удален"

def test_add_product():
    catalog.database.products.insert_one = MagicMock(return_value=[{"article": "Пизда", "name": "манда", "quantity": 123}])
    dto = ProductCreateDTO(article="Пизда", name="манда", quantity=123)
    result = catalog.add_product(dto)
    assert result == "Товар добавлен в каталог"

def test_edit_product():
    catalog.database.products.update_one = MagicMock(return_value=[{"article": "Пизда", "quantity": 123}])
    dto = ProductUpdateDTO(article="Пизда", quantity=80)
    result = catalog.edit_product(dto)
    assert result == f"Для товара {dto.article}, было задано новое количество - {dto.quantity}"

def test_search_product_found():
    catalog.database.products.find = MagicMock(return_value=[{"name": "Пизда", "article": "манда", "quantity": 123}])
    dto = ProductGetArticleDTO(article="манда")

    result = catalog.search_product(dto)
    assert result == f"{"Пизда"} - {"манда"} - {123}\n\n"

def test_search_product_not_found():
    catalog.database.products.find = MagicMock(return_value=[{"name": "Пизда", "article": "манда", "quantity": 123}])
    dto = ProductGetArticleDTO(article="Рыготня")

    result = catalog.search_product(dto)
    assert result == "Товар не найден"