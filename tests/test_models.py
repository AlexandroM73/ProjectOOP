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


class TestCategory(unittest.TestCase):
    def setUp(self):
        """Создаём тестовые объекты перед каждым тестом."""
        self.product1 = Product("Ноутбук", "Игровой ноутбук", 99999.99, 5)
        self.product2 = Product("Мышь", "Беспроводная мышь", 1999.99, 20)

    def test_category_init_with_products(self):
        """Проверяем инициализацию категории с списком товаров."""
        category = Category("Электроника", "Все виды электронных устройств", [self.product1, self.product2])
        self.assertEqual(category.name, "Электроника")
        self.assertEqual(category.description, "Все виды электронных устройств")
        self.assertEqual(len(category._Category__products), 2)

    def test_category_init_without_products(self):
        """Проверяем инициализацию категории без товаров."""
        category = Category("Книги", "Художественная литература")
        self.assertEqual(category.name, "Книги")
        self.assertEqual(category.description, "Художественная литература")
        self.assertEqual(len(category._Category__products), 0)

    def test_add_product(self):
        """Проверяем добавление товара в категорию."""
        category = Category("Электроника", "Устройства")
        category.add_product(self.product1)
        self.assertIn(self.product1, category._Category__products)

    def test_add_invalid_product(self):
        """Проверяем добавление некорректного объекта в категорию."""
        category = Category("Электроника", "Устройства")
        with self.assertRaises(TypeError):
            category.add_product("Не товар")

    def test_products_getter_empty(self):
        """Проверяем геттер products для пустой категории."""
        category = Category("Пустая", "Категория без товаров")
        self.assertEqual(category.products, "В категории нет товаров.")

    def test_products_getter_with_items(self):
        """Проверяем геттер products с товарами."""
        category = Category("Электроника", "Устройства", [self.product1])
        expected_output = "Ноутбук, 99999.99 руб. Остаток: 5 шт."
        self.assertEqual(category.products, expected_output)

    def test_get_product_count(self):
        """Проверяем метод get_product_count."""
        category = Category("Электроника", "Устройства", [self.product1, self.product2])
        self.assertEqual(category.get_product_count(), 2)


if __name__ == '__main__':
    unittest.main()

# class TestProduct:
#     def test_product_initialization(self):
#         """Проверяет корректность инициализации объекта Product."""
#         product = Product("Смартфон", "Описание смартфона", 50000.0, 10)
#
#         assert product.name == "Смартфон"
#         assert product.description == "Описание смартфона"
#         assert product.price == 50000.0
#         assert product.quantity == 10
#
#     def test_product_price_type(self):
#         """Проверяет тип цены — должен быть float."""
#         product = Product("Смартфон", "Описание", 50000, 10)
#         assert isinstance(product.price, float)
#
#     def test_product_quantity_type(self):
#         """Проверяет тип количества — должен быть int."""
#         product = Product("Смартфон", "Описание", 50000, 10)
#         assert isinstance(product.quantity, int)
#
#
# class TestCategory:
#     @pytest.fixture
#     def setup_products(self):
#         """Фикстура для создания тестовых продуктов."""
#         return [
#             Product("Смартфон 1", "Описание 1", 30000.0, 5),
#             Product("Смартфон 2", "Описание 2", 40000.0, 3),
#             Product("Смартфон 3", "Описание 3", 50000.0, 2)
#         ]
#
#     def test_category_initialization(self, setup_products):
#         """Проверяет корректность инициализации объекта Category."""
#         category = Category(
#             "Смартфоны", "Категория смартфонов", setup_products
#         )
#
#         assert category.name == "Смартфоны"
#         assert category.description == "Категория смартфонов"
#         assert len(category.products) == 3
#         assert isinstance(category.products, list)
#         assert all(isinstance(p, Product) for p in category.products)
#
#     def test_category_count_increases(self, setup_products):
#         """Проверяет, что счётчик категорий
#             увеличивается при создании новой категории."""
#         initial_count = Category.category_count
#         Category("Новая категория", "Описание", setup_products[:1])
#         assert Category.category_count == initial_count + 1
#
#     def test_product_count_increases_correctly(self, setup_products):
#         """Проверяет, что счётчик товаров увеличивается
#             на количество товаров в новой категории."""
#         initial_product_count = Category.product_count
#         num_products = len(setup_products)
#         Category("Ещё одна категория", "Описание", setup_products)
#         assert Category.product_count == initial_product_count + num_products
#
#     def test_multiple_categories_count(self):
#         """Проверяет подсчёт категорий и товаров
#                 при создании нескольких категорий."""
#         Category.category_count = 0
#         Category.product_count = 0
#
#         products1 = [
#             Product("Товар 1", "Описание 1", 1000.0, 5),
#             Product("Товар 2", "Описание 2", 2000.0, 3)
#         ]
#         products2 = [
#             Product("Товар 3", "Описание 3", 1500.0, 4),
#             Product("Товар 4", "Описание 4", 2500.0, 2),
#             Product("Товар 5", "Описание 5", 3000.0, 1)
#         ]
#
#         Category("Категория 1", "Описание 1", products1)
#         Category("Категория 2", "Описание 2", products2)
#
#         assert Category.category_count == 2
#         assert Category.product_count == 5  # 2 + 3 товара
#
#     def test_empty_category(self):
#         """Проверяет создание категории без товаров."""
#         initial_category_count = Category.category_count
#         initial_product_count = Category.product_count
#
#         empty_category = Category("Пустая категория", "Без товаров", [])
#
#         assert Category.category_count == initial_category_count + 1
#         assert Category.product_count == initial_product_count
#         assert len(empty_category.products) == 0
#
#     def test_single_product_category(self):
#         """Проверяет категорию с одним товаром."""
#         single_product = [Product("Единственный товар", "Описание", 1000.0, 1)]
#         initial_product_count = Category.product_count
#
#         single_category = Category(
#             "Одиночный товар", "Одна позиция", single_product
#         )
#
#         assert Category.product_count == initial_product_count + 1
#         assert len(single_category.products) == 1
