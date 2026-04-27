import json
from src.data_load import load_data_from_json
from main import Product, Category


def test_load_data_from_json_file_not_found():
    """Тест обработки ошибки отсутствия файла."""
    categories = load_data_from_json("nonexistent.json")
    assert categories == []


def test_product_creation():
    """Тест создания объекта Product."""
    product = Product("Test Phone", "Test description", 10000.0, 10)
    assert product.name == "Test Phone"
    assert product.price == 10000.0
    assert product.quantity == 10
    assert isinstance(product.price, float)
    assert isinstance(product.quantity, int)


def test_category_creation():
    """Тест создания объекта Category."""
    product = Product("Test Phone", "Test", 10000.0, 10)
    category = Category("Test Category", "Test desc", [product])
    assert category.name == "Test Category"
    assert category.description == "Test desc"
    assert len(category.products) == 1
    assert isinstance(category.products, list)


def test_load_data_from_json_valid_old_format():
    """Тест загрузки данных в старом формате (с ключом 'categories')."""
    data = {
        "categories": [
            {
                "name": "Смартфоны",
                "description": "Мобильные устройства",
                "products": [
                    {
                        "name": "Samsung Galaxy S23 Ultra",
                        "description": "256GB, Серый цвет, 200MP камера",
                        "price": 180000.0,
                        "quantity": 5
                    }
                ]
            }
        ]
    }
    with open("test_products_old.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_data_from_json("test_products_old.json")

    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"
    assert categories[0].description == "Мобильные устройства"
    assert len(categories[0].products) == 1
    assert isinstance(categories[0].products[0], Product)
    assert categories[0].products[0].name == "Samsung Galaxy S23 Ultra"


def test_load_data_from_json_valid_new_format():
    """Тест загрузки данных в новом формате (массив категорий)."""
    data = [
        {
            "name": "Ноутбуки",
            "description": "Портативные компьютеры",
            "products": [
                {
                    "name": "MacBook Pro 16",
                    "description": "M2 Pro, 1TB SSD",
                    "price": 250000.0,
                    "quantity": 3
                }
            ]
        }
    ]
    with open("test_products_new.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_data_from_json("test_products_new.json")

    assert len(categories) == 1
    assert categories[0].name == "Ноутбуки"
    assert len(categories[0].products) == 1


def test_load_data_from_json_missing_category_fields():
    """Тест обработки категорий с отсутствующими обязательными полями."""
    data = {
        "categories": [
            {"name": "Пустая категория"},  # Нет description и products
            {
                "description": "Без названия",
                "products": []
            },  # Нет name
            {
                "name": "Без описания",
                "products": []
            }  # Нет description
        ]
    }
    with open("test_missing_categories.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_data_from_json("test_missing_categories.json")
    assert len(categories) == 0


def test_load_data_from_json_missing_product_fields():
    """Тест обработки товаров с отсутствующими обязательными полями."""
    data = {
        "categories": [
            {
                "name": "Тесты",
                "description": "Категория для тестирования",
                "products": [
                    {"name": "Товар без полей"},  # Отсутствуют price, quantity, description
                    {
                        "price": 1000.0,
                        "quantity": 5
                    }  # Отсутствуют name, description
                ]
            }
        ]
    }
    with open("test_missing_products.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_data_from_json("test_missing_products.json")
    # Должна создаться категория, но без товаров
    assert len(categories) == 1
    assert len(categories[0].products) == 0


def test_load_data_from_json_empty_file():
    """Тест обработки пустого JSON‑файла."""
    with open("test_empty.json", "w") as f:
        f.write("")

    categories = load_data_from_json("test_empty.json")
    assert categories == []


def test_load_data_from_json_invalid_json():
    """Тест обработки некорректного JSON."""
    with open("test_invalid.json", "w") as f:
        f.write("некорректный json {]")

    categories = load_data_from_json("test_invalid.json")
    assert categories == []


def test_load_data_from_json_multiple_categories():
    """Тест загрузки нескольких категорий."""
    data = {
        "categories": [
            {
                "name": "Категория 1",
                "description": "Описание 1",
                "products": [
                    {
                        "name": "Товар 1",
                        "price": 100.0,
                        "quantity": 1,
                        "description": "Описание товара 1"
                    }
                ]
            },
            {
                "name": "Категория 2",
                "description": "Описание 2",
                "products": [
                    {
                        "name": "Товар 2",
                        "price": 200.0,
                        "quantity": 2,
                        "description": "Описание товара 2"
                    }
                ]
            }
        ]
    }
    with open("test_multiple.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_data_from_json("test_multiple.json")
    assert len(categories) == 2
    assert categories[0].name == "Категория 1"
    assert categories[1].name == "Категория 2"
    assert len(categories[0].products) == 1
    assert len(categories[1].products) == 1


def test_load_data_from_json_price_conversion():
    """Тест преобразования цены в float (из int и str)."""
    data = {
        "categories": [
            {
                "name": "Цены",
                "description": "Тестирование типов цен",
                "products": [
                    {
                        "name": "Цена как int",
                        "price": 1000,  # int
                        "quantity": 1,
                        "description": "Тест"
                    },
                    {
                        "name": "Цена как строка",
                        "price": "2000.50",  # str
                        "quantity": 1,
                        "description": "Тест"
                    }
                ]
            }
        ]
    }
    with open("test_prices.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    categories = load_data_from_json("test_prices.json")
    assert len(categories) == 1
    assert len(categories[0].products) == 2

    # Проверяем первый товар (цена была int)
    product1 = categories[0].products[0]
    assert product1.name == "Цена как int"
    assert product1.price == 1000.0  # Должно быть преобразовано в float
    assert isinstance(product1.price, float)

    # Проверяем второй товар (цена была строкой)
    product2 = categories[0].products[1]
    assert product2.name == "Цена как строка"
    assert product2.price == 2000.50  # Должно быть преобразовано в float
    assert isinstance(product2.price, float)
