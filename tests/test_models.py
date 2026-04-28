import unittest
from unittest.mock import patch

from src.models import Product, Category


class TestProduct(unittest.TestCase):
    def setUp(self):
        """Создаём тестовый объект Product перед каждым тестом."""
        self.product = Product("Смартфон", "Современный смартфон", 49999.99, 10)

    def test_price_getter(self):
        """Проверяем, что геттер возвращает корректное значение."""
        self.assertEqual(self.product.price, 49999.99)

    def test_price_setter_positive(self):
        """Проверяем установку положительной цены."""
        self.product.price = 55000.00
        self.assertEqual(self.product.price, 55000.00)

    def test_price_setter_zero(self):
        """Проверяем обработку нулевой цены."""
        with self.assertLogs(level='INFO') as log:
            self.product.price = 0
            self.assertIn("Цена не должна быть нулевая или отрицательная", log.output[0])
        # Цена не должна измениться
        self.assertEqual(self.product.price, 49999.99)

    def test_price_setter_negative(self):
        """Проверяем обработку отрицательной цены."""
        with self.assertLogs(level='INFO') as log:
            self.product.price = -5000
            self.assertIn("Цена не должна быть нулевая или отрицательная", log.output[0])
        # Цена не должна измениться
        self.assertEqual(self.product.price, 49999.99)

    @patch('builtins.input', return_value='y')
    def test_price_lower_confirm(self, mock_input):
        """Проверяем подтверждение понижения цены (ответ 'y')."""
        self.product.price = 45000.00
        self.assertEqual(self.product.price, 45000.00)

    @patch('builtins.input', return_value='n')
    def test_price_lower_cancel(self, mock_input):
        """Проверяем отмену понижения цены (ответ 'n')."""
        original_price = self.product.price
        self.product.price = 40000.00
        # Цена не должна измениться
        self.assertEqual(self.product.price, original_price)

    @patch('builtins.input', return_value='other')
    def test_price_lower_invalid_response(self, mock_input):
        """Проверяем обработку некорректного ответа (не 'y' и не 'n')."""
        original_price = self.product.price
        self.product.price = 35000.00
        # Цена не должна измениться
        self.assertEqual(self.product.price, original_price)

    def test_initial_price_negative(self):
        """Проверяем создание продукта с отрицательной ценой."""
        with self.assertRaises(ValueError):
            Product("Товар", "Описание", -1000, 5)

    def test_product_initialization(self):
        """Проверяет корректность инициализации объекта Product."""
        product = Product("Смартфон", "Описание смартфона", 50000.0, 10)

        assert product.name == "Смартфон"
        assert product.description == "Описание смартфона"
        assert product.price == 50000.0
        assert product.quantity == 10

    def test_product_price_type(self):
        """Проверяет тип цены — должен быть float."""
        product = Product("Смартфон", "Описание", 50000, 10)
        assert isinstance(product.price, float)

    def test_product_quantity_type(self):
        """Проверяет тип количества — должен быть int."""
        product = Product("Смартфон", "Описание", 50000, 10)
        assert isinstance(product.quantity, int)


class TestCategory(unittest.TestCase):
    def setUp(self):
        Category.product_counter = 0  # Сброс счётчика перед каждым тестом

    def test_products_getter_returns_formatted_string(self):
        """Проверяем, что геттер products возвращает строку в правильном формате."""
        category = Category("Смартфоны", "Мобильные устройства")
        product = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5)
        category.add_product(product)

        expected = "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт."
        self.assertEqual(category.products, expected)

    def test_multiple_products_formatted(self):
        """Проверяем форматирование нескольких товаров."""
        category = Category("Ноутбуки", "Портативные компьютеры")
        product1 = Product("MacBook Pro 16", "M2 Pro, 1TB SSD", 250000.0, 3)
        product2 = Product("Dell XPS 13", "Intel i7, 512GB SSD", 150000.0, 2)
        category.add_product(product1)
        category.add_product(product2)

        expected_lines = [
            "MacBook Pro 16, 250000.0 руб. Остаток: 3 шт.",
            "Dell XPS 13, 150000.0 руб. Остаток: 2 шт."
        ]
        expected = "\n".join(expected_lines)
        self.assertEqual(category.products, expected)

    def test_add_product_updates_counter(self):
        """Проверяем, что добавление продукта увеличивает счётчик."""
        category = Category("Тесты", "Описание")
        product = Product("Тест", "Описание", 100.0, 5)

        category.add_product(product)
        self.assertEqual(category.get_product_count(), 1)
        self.assertEqual(Category.get_total_product_count(), 1)

        # Добавляем ещё один продукт
        product2 = Product("Тест 2", "Описание 2", 200.0, 3)
        category.add_product(product2)
        self.assertEqual(category.get_product_count(), 2)
        self.assertEqual(Category.get_total_product_count(), 2)

    def test_category_init_without_products(self):
        """Проверяем инициализацию категории без товаров."""
        category = Category("Книги", "Художественная литература")
        self.assertEqual(category.name, "Книги")
        self.assertEqual(category.description, "Художественная литература")
        self.assertEqual(len(category._Category__products), 0)

    def test_add_invalid_product(self):
        """Проверяем добавление некорректного объекта в категорию."""
        category = Category("Электроника", "Устройства")
        with self.assertRaises(TypeError):
            category.add_product("Не товар")


if __name__ == '__main__':
    unittest.main()
