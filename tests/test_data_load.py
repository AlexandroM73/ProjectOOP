import json
import os
import unittest
from src.data_load import load_data_from_json
from src.models import Product, Category


class TestDataLoad(unittest.TestCase):
    """Тесты для функции load_data_from_json."""

    def setUp(self):
        """Создаём временные файлы для тестов."""
        self.test_files = []

    def tearDown(self):
        """Удаляем временные файлы после тестов."""
        for filename in self.test_files:
            if os.path.exists(filename):
                os.remove(filename)

    def create_test_file(self, filename: str, data):
        """Вспомогательный метод для создания тестовых JSON‑файлов."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        self.test_files.append(filename)

    def test_file_not_found(self):
        """Тест обработки ошибки отсутствия файла."""
        categories = load_data_from_json("nonexistent.json")
        self.assertEqual(categories, [])

    def test_empty_file(self):
        """Тест обработки пустого JSON‑файла."""
        self.create_test_file("test_empty.json", "")
        categories = load_data_from_json("test_empty.json")
        self.assertEqual(categories, [])

    def test_invalid_json(self):
        """Тест обработки некорректного JSON."""
        with open("test_invalid.json", "w", encoding="utf-8") as f:
            f.write("некорректный json {]")
        self.test_files.append("test_invalid.json")

        categories = load_data_from_json("test_invalid.json")
        self.assertEqual(categories, [])

    def test_product_creation(self):
        """Тест создания объекта Product."""
        product = Product("Test Phone", "Test description", 10000.0, 10)
        self.assertEqual(product.name, "Test Phone")
        self.assertEqual(product.price, 10000.0)
        self.assertEqual(product.quantity, 10)
        self.assertIsInstance(product.price, float)
        self.assertIsInstance(product.quantity, int)

    def test_category_creation(self):
        """Тест создания объекта Category."""
        product = Product("Test Phone", "Test", 10000.0, 10)
        category = Category("Test Category", "Test desc", [product])
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.description, "Test desc")
        self.assertEqual(len(category._Category__products), 1)
        # products — строка, а не список
        self.assertIsInstance(category.products, str)

    def test_valid_old_format(self):
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
        self.create_test_file("test_products_old.json", data)

        categories = load_data_from_json("test_products_old.json")

        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].name, "Смартфоны")
        self.assertEqual(categories[0].description, "Мобильные устройства")
        self.assertEqual(len(categories[0]._Category__products), 1)
        product = categories[0]._Category__products[0]
        self.assertIsInstance(product, Product)
        self.assertEqual(product.name, "Samsung Galaxy S23 Ultra")

    def test_valid_new_format(self):
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
        self.create_test_file("test_products_new.json", data)

        categories = load_data_from_json("test_products_new.json")

        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].name, "Ноутбуки")
        self.assertEqual(len(categories[0]._Category__products), 1)

    def test_missing_category_fields(self):
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
        self.create_test_file("test_missing_categories.json", data)

        categories = load_data_from_json("test_missing_categories.json")
        self.assertEqual(len(categories), 0)

    def test_missing_product_fields(self):
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
        self.create_test_file("test_missing_products.json", data)

        categories = load_data_from_json("test_missing_products.json")
        # Должна создаться категория, но без товаров
        self.assertEqual(len(categories), 1)
        self.assertEqual(len(categories[0]._Category__products), 0)

    def test_multiple_categories(self):
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
        self.create_test_file("test_multiple.json", data)

        categories = load_data_from_json("test_multiple.json")
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0].name, "Категория 1")
        self.assertEqual(categories[1].name, "Категория 2")
        self.assertEqual(len(categories[0]._Category__products), 1)
        self.assertEqual(len(categories[1]._Category__products), 1)

        def test_price_conversion(self):
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
            self.create_test_file("test_prices.json", data)

            categories = load_data_from_json("test_prices.json")
            self.assertEqual(len(categories), 1)
            self.assertEqual(len(categories[0]._Category__products), 2)

            # Проверяем первый товар (цена была int)
            product1 = categories[0]._Category__products[0]
            self.assertEqual(product1.name, "Цена как int")
            self.assertEqual(product1.price, 1000.0)  # Должно быть преобразовано в float
            self.assertIsInstance(product1.price, float)

            # Проверяем второй товар (цена была строкой)
            product2 = categories[0]._Category__products[1]
            self.assertEqual(product2.name, "Цена как строка")
            self.assertEqual(product2.price, 2000.50)  # Должно быть преобразовано в float
            self.assertIsInstance(product2.price, float)
