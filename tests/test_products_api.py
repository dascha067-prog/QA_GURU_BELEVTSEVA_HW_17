import pytest
import requests
from api.schemas import Product, ProductPartial
from tests.test_schemas import BASE_URL


# ---------- GET ----------

def test_get_product_positive():
    response = requests.get(f"{BASE_URL}/products/1")

    assert response.status_code == 200

    product = Product.model_validate(response.json())

    assert product.id == 1
    assert product.title == "Fjallraven - Foldsack No. 1 Backpack, Fits 15 Laptops"
    assert product.price == 109.95
    assert product.description
    assert product.category == "men's clothing"
    assert product.image.startswith("https://")


@pytest.mark.xfail(
    reason="API не валидирует тип id (ожидаем 400, но приходит 200)",
    strict=True
)
def test_get_product_negative_invalid_id():
    # Act - выполняем GET-запрос с невалидным id (строка вместо числа)
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
    # Arrange - подгаталиваем тело запроса для создани нового продукта
    payload = {
        "title": "New product",
        "price": 99.9,
        "description": "Test product",
        "category": "electronics",
        "image": "https://example.com/image.png",
    }

    response = requests.post(f"{BASE_URL}/products", json=payload)

    assert response.status_code == 201

    product = Product.model_validate(response.json())

    # Act - проверяем, что API вернул ИМЕННО то, что отправили
    assert product.title == payload["title"]
    assert product.price == payload["price"]
    assert product.description == payload["description"]
    assert product.category == payload["category"]
    assert product.image == payload["image"]


# ---------- PUT ----------

def test_update_product():
    # Arrange - данные для частичного обновления продукта
    payload = {
        "title": "Updated title",
        "price": 199.9,
    }
    # Act -обновляем продукт
    response = requests.put(f"{BASE_URL}/products/1", json=payload)

    assert response.status_code == 200

    product = ProductPartial.model_validate(response.json())

    # Act - проверяем обновлённые значения
    assert product.title == payload["title"]
    assert product.price == payload["price"]


# ---------- DELETE ----------

def test_delete_product():
    response = requests.delete(f"{BASE_URL}/products/1")

    assert response.status_code == 200
