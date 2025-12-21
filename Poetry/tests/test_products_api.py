import pytest
import requests

# Импортируем Pydantic-схему продукта
# Она нужна для проверки структуры ответа (контракт API)
from Poetry.api.schemas import Product, ProductPartial

# Базовый URL тестируемого API
BASE_URL = "https://fakestoreapi.com"


# ---------- GET ----------

def test_get_product_positive():
    # Act — выполняем GET-запрос на получение продукта с валидным id
    response = requests.get(f"{BASE_URL}/products/1")

    # Assert — проверяем, что запрос успешный
    assert response.status_code == 200

    # Assert — проверяем, что тело ответа соответствует схеме Product
    # (поля присутствуют и имеют корректные типы)
    Product.model_validate(response.json())


@pytest.mark.xfail(
    reason="API не валидирует тип id: ожидается 400, но возвращается 200",
    strict=True
)
def test_get_product_negative_invalid_id():
    # Act — выполняем GET-запрос с невалидным id (строка вместо числа)
    response = requests.get(f"{BASE_URL}/products/abc")

    # Assert — ожидаем ошибку клиента (400),
    # но тест помечен xfail, так как API фактически возвращает 200
    assert response.status_code == 400


def test_get_product_non_existing_id_returns_404():
    # Arrange
    product_id = 999999
    url = f"{BASE_URL}/products/{product_id}"

    # Act
    response = requests.get(url)

    # Assert
    assert response.status_code == 404


@pytest.mark.xfail(
    reason="API не возвращает 404 для несуществующего id",
    strict=True
)
def test_get_product_non_existing_id_returns_404():
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

    # Act — выполняем POST-запрос на создание продукта
    response = requests.post(f"{BASE_URL}/products", json=payload)

    # Assert — проверяем, что продукт успешно создан
    assert response.status_code == 201

    # Assert — проверяем, что ответ соответствует схеме Product
    Product.model_validate(response.json())


# ---------- PUT ----------

def test_update_product():
    # Arrange — данные для частичного обновления продукта
    payload = {
        "title": "Updated title",
        "price": 199.9
    }

    # Act — обновляем продукт
    response = requests.put(f"{BASE_URL}/products/1", json=payload)

    # Assert — успешное обновление
    assert response.status_code == 200

    # Assert — ответ соответствует ЧАСТИЧНОЙ схеме продукта
    ProductPartial.model_validate(response.json())


# ---------- DELETE ----------

def test_delete_product():
    # Act — выполняем DELETE-запрос на удаление продукта
    response = requests.delete(f"{BASE_URL}/products/1")

    # Assert — проверяем, что продукт удалён
    # API может вернуть 200 (с телом) или 204 (без тела ответа)
    assert response.status_code in (200, 204)
