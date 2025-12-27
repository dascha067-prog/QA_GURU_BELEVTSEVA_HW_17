import pytest
import requests
from api.schemas import Product, ProductPartial

BASE_URL = "https://fakestoreapi.com"


# ---------- GET ----------

def test_get_product_positive():
    response = requests.get(f"{BASE_URL}/products/1")

    assert response.status_code == 200

    product = Product.model_validate(response.json())

    assert product.id == 1
    assert product.price > 0
    assert product.title


@pytest.mark.xfail(
    reason="API не валидирует тип id: ожидается 400, но возвращается 200",
    strict=True
)
def test_get_product_negative_invalid_id():
    # Act — выполняем GET-запрос с невалидным id (строка вместо числа)
    response = requests.get(f"{BASE_URL}/products/abc")

    assert response.status_code == 400


@pytest.mark.xfail(
    reason="API не возвращает 404 для несуществующего id",
    strict=True
)
def test_get_product_non_existing_id():
    response = requests.get(f"{BASE_URL}/products/999999")
    assert response.status_code == 404


# ---------- POST ----------

def test_create_product():
    # Arrange — подготавливаем тело запроса для создания нового продукта
    payload = {
        "title": "New product",
        "price": 99.9,
        "description": "Test product",
        "category": "electronics",
        "image": "https://example.com/image.png"
    }

    response = requests.post(f"{BASE_URL}/products", json=payload)

    assert response.status_code == 201

    product = Product.model_validate(response.json())

    assert product.title == payload["title"]
    assert product.price == payload["price"]


# ---------- PUT ----------

def test_update_product():
    # Arrange — данные для частичного обновления продукта
    payload = {
        "title": "Updated title",
        "price": 199.9
    }

    # Act — обновляем продукт
    response = requests.put(f"{BASE_URL}/products/1", json=payload)

    assert response.status_code == 200

    ProductPartial.model_validate(response.json())


# ---------- DELETE ----------

def test_delete_product():
    response = requests.delete(f"{BASE_URL}/products/1")

    assert response.status_code in (200, 204)
