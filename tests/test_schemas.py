import requests
from api.schemas import Product

BASE_URL = "https://fakestoreapi.com"


def test_schema_single_product():
    response = requests.get(f"{BASE_URL}/products/1")

    product = Product.model_validate(response.json())

    assert product.id == 1


def test_schema_product_list():
    response = requests.get(f"{BASE_URL}/products")

    data = response.json()
    assert isinstance(data, list)

    product = Product.model_validate(data[0])
    assert product.id > 0
