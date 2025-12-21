import requests

from Poetry.api.schemas import Product

BASE_URL = "https://fakestoreapi.com"


# Проверка схемы одиночного продукта (GET /products/{id})
def test_schema_single_product():
    # Arrange — готовим URL для запроса одного продукта
    product_id = 1
    url = f"{BASE_URL}/products/{product_id}"

    # Act — выполняем GET-запрос
    response = requests.get(url)

    # Assert — проверяем, что ответ соответствует схеме Product
    # Pydantic валидирует наличие полей и их типы
    Product.model_validate(response.json())


# Проверка схемы списка продуктов (GET /products)
def test_schema_product_list():
    # Arrange — URL для получения списка продуктов
    url = f"{BASE_URL}/products"

    # Act — выполняем GET-запрос
    response = requests.get(url)

    # Assert — проверяем, что ответ является списком
    data = response.json()
    assert isinstance(data, list)

    # Проверяем схему хотя бы одного элемента списка
    Product.model_validate(data[0])
