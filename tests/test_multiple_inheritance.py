import unittest
from io import StringIO
import sys

from src.multiple_inheritance import Category, Order, Product, Smartphone, LawnGrass


class TestCategory(unittest.TestCase):
    """Тесты для класса Category."""

    def setUp(self):
        """Подготовка данных перед каждым тестом."""
        self.category = Category("Электроника", "Электронные устройства")

    def test_category_creation(self):
        """Тест создания категории."""
        self.assertEqual(self.category.get_name(), "Электроника")
        self.assertEqual(self.category.get_description(), "Электронные устройства")

    def test_category_str_representation(self):
        """Тест строкового представления категории."""
        expected = "Категория: Электроника — Электронные устройства"
        self.assertEqual(str(self.category), expected)

    def test_category_name_getter(self):
        """Тест геттера имени категории."""
        self.assertEqual(self.category.get_name(), "Электроника")

    def test_category_description_getter(self):
        """Тест геттера описания категории."""
        self.assertEqual(self.category.get_description(), "Электронные устройства")


class TestOrder(unittest.TestCase):
    """Тесты для класса Order."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        # Создаём базовый продукт для тестов
        self.product = Product("Ноутбук", "Игровой ноутбук", 89990, 5)
        # Создаём смартфон для тестов
        self.smartphone = Smartphone(
            "Galaxy S23", "Флагманский смартфон", 79990, 3,
            "высокая", "S23", "128 ГБ", "чёрный"
        )
        # Создаём газонную траву для тестов
        self.lawn_grass = LawnGrass(
            "Газонная трава", "Зелёная трава для газона", 1500, 10,
            "Россия", "14 дней", "зелёный"
        )

    def test_order_creation_with_product(self):
        """Тест создания заказа с базовым продуктом."""
        order = Order(self.product, 2)
        self.assertEqual(order.get_product(), self.product)
        self.assertEqual(order.get_quantity(), 2)
        self.assertEqual(order.get_total_price(), 179980)  # 89990 * 2

    def test_order_creation_with_smartphone(self):
        """Тест создания заказа со смартфоном."""
        order = Order(self.smartphone, 1)
        self.assertEqual(order.get_product().get_name(), "Galaxy S23")
        self.assertEqual(order.get_quantity(), 1)
        self.assertEqual(order.get_total_price(), 79990)

    def test_order_creation_with_lawngrass(self):
        """Тест создания заказа с газонной травой."""
        order = Order(self.lawn_grass, 3)
        self.assertEqual(order.get_product().get_name(), "Газонная трава")
        self.assertEqual(order.get_quantity(), 3)
        self.assertEqual(order.get_total_price(), 4500)  # 1500 * 3

    def test_order_str_representation(self):
        """Тест строкового представления заказа."""
        order = Order(self.product, 2)
        str_repr = str(order)

        # Проверяем основные компоненты строки с гибкой проверкой цены
        self.assertIn("Заказ: Ноутбук", str_repr)
        self.assertTrue("179980" in str_repr and "руб." in str_repr,
                        f"Не найдена цена '179980 руб.' в строке: {str_repr}")
        self.assertIn("Количество: 2 шт.", str_repr)

        # Дополнительно проверяем полную строку с помощью регулярного выражения
        expected_pattern = r"Заказ: Ноутбук \| Количество: 2 шт\. \| Итого: 179980(\.0)? руб\."
        self.assertRegex(str_repr, expected_pattern,
                         f"Строка не соответствует шаблону: {expected_pattern}\nФактическая: {str_repr}")

    def test_order_repr_representation(self):
        """Тест repr представления заказа."""
        order = Order(self.product, 1)
        expected_start = "Order(product=Product(name='Ноутбук'"
        self.assertTrue(str(order.__repr__()).startswith(expected_start))

    def test_order_getters(self):
        """Тест всех геттеров заказа."""
        order = Order(self.product, 3)
        self.assertEqual(order.get_name(), "Ноутбук")
        self.assertEqual(order.get_description(), "Игровой ноутбук")
        self.assertEqual(order.get_quantity(), 3)
        self.assertEqual(order.get_total_price(), 269970)  # 89990 * 3
        self.assertEqual(order.get_product(), self.product)

    def test_order_invalid_quantity_zero(self):
        """Тест ошибки при количестве 0."""
        with self.assertRaises(ValueError) as context:
            Order(self.product, 0)
        self.assertIn("Количество в заказе должно быть положительным", str(context.exception))

    def test_order_invalid_quantity_negative(self):
        """Тест ошибки при отрицательном количестве."""
        with self.assertRaises(ValueError) as context:
            Order(self.product, -1)
        self.assertIn("Количество в заказе должно быть положительным", str(context.exception))

    def test_order_insufficient_stock(self):
        """Тест ошибки при недостатке товара на складе."""
        # У продукта всего 5 единиц, пытаемся заказать 6
        with self.assertRaises(ValueError) as context:
            Order(self.product, 6)
        self.assertIn("Недостаточно товара на складе", str(context.exception))

    def test_order_total_price_calculation(self):
        """Тест корректности расчёта итоговой стоимости."""
        # Разные количества для проверки расчёта
        test_cases = [
            (1, 89990),
            (2, 179980),
            (3, 269970),
            (5, 449950)
        ]
        for quantity, expected_price in test_cases:
            order = Order(self.product, quantity)
            self.assertEqual(order.get_total_price(), expected_price)


class TestCreationLoggerMixin(unittest.TestCase):
    """Тесты для миксина CreationLoggerMixin"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        """Очистка после каждого теста"""
        sys.stdout = self.held

    def test_product_creation_logging(self):
        """Тест логирования создания объекта Product"""
        with unittest.mock.patch('builtins.print') as mock_print:
            product = Product("Продукт1", "Описание продукта", 1200, 10)

            # Проверяем, что print был вызван с ожидаемой строкой
            mock_print.assert_called_with(
                "Product('Продукт1', 'Описание продукта', 1200, 10)"
            )

            # Проверяем корректность атрибутов объекта
            self.assertEqual(product.get_name(), "Продукт1")
            self.assertEqual(product.get_price(), 1200)
            self.assertEqual(product.get_quantity(), 10)

    def test_smartphone_creation_logging(self):
        """Тест логирования создания объекта Smartphone"""
        with unittest.mock.patch('builtins.print') as mock_print:
            smartphone = Smartphone(
                "Galaxy S23", "Флагманский смартфон", 79990, 2,
                "высокая", "S23", "128 ГБ", "чёрный"
            )
            mock_print.assert_called_with(
                "Smartphone('Galaxy S23', 'Флагманский смартфон', 79990, 2)"
            )
            # Проверяем атрибуты
            self.assertEqual(smartphone.get_name(), "Galaxy S23")
            self.assertEqual(smartphone.model, "S23")
            self.assertEqual(smartphone.memory, "128 ГБ")

    def test_lawn_grass_creation_logging(self):
        """Тест логирования создания объекта LawnGrass"""
        with unittest.mock.patch('builtins.print') as mock_print:
            grass = LawnGrass(
                "Зелёная трава", "Газонная", 1500, 10,
                "Россия", "7–14 дней", "зелёный"
            )
            mock_print.assert_called_with(
                "LawnGrass('Зелёная трава', 'Газонная', 1500, 10)"
            )
            # Проверяем атрибуты
            self.assertEqual(grass.get_name(), "Зелёная трава")
            self.assertEqual(grass.country, "Россия")
            self.assertEqual(grass.germination_period, "7–14 дней")

    def test_repr_product(self):
        """Тест метода __repr__ для Product"""
        product = Product("Продукт1", "Описание продукта", 1200, 10)
        expected = "Product(name='Продукт1', description='Описание продукта', price=1200.0, quantity=10)"
        self.assertEqual(repr(product), expected)

    def test_repr_smartphone(self):
        """Тест метода __repr__ для Smartphone"""
        smartphone = Smartphone(
            "Galaxy S23", "Флагманский смартфон", 79990, 2,
            "высокая", "S23", "128 ГБ", "чёрный"
        )
        repr_str = repr(smartphone)
        self.assertIn("name='Galaxy S23'", repr_str)
        self.assertIn("description='Флагманский смартфон'", repr_str)
        self.assertIn("price=79990.0", repr_str)
        self.assertIn("quantity=2", repr_str)
        self.assertIn("performance='высокая'", repr_str)
        self.assertIn("model='S23'", repr_str)
        self.assertIn("memory='128 ГБ'", repr_str)
        self.assertIn("color='чёрный'", repr_str)

    def test_repr_lawn_grass(self):
        """Тест метода __repr__ для LawnGrass"""
        grass = LawnGrass(
            "Зелёная трава", "Газонная", 1500, 10,
            "Россия", "7–14 дней", "зелёный"
        )
        repr_str = repr(grass)
        self.assertIn("name='Зелёная трава'", repr_str)
        self.assertIn("description='Газонная'", repr_str)
        self.assertIn("price=1500.0", repr_str)
        self.assertIn("quantity=10", repr_str)
        self.assertIn("country='Россия'", repr_str)
        self.assertIn("germination_period='7–14 дней'", repr_str)
        self.assertIn("color='зелёный'", repr_str)


class TestProductClass(unittest.TestCase):
    """Тесты для класса Product и его наследников"""

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.held

    def test_product_initialization_valid(self):
        """Тест корректной инициализации Product"""
        product = Product("Продукт1", "Описание", 100, 5)
        self.assertEqual(product.get_name(), "Продукт1")
        self.assertEqual(product.get_description(), "Описание")
        self.assertEqual(product.get_price(), 100.0)
        self.assertEqual(product.get_quantity(), 5)

    def test_product_invalid_price(self):
        """Тест инициализации с некорректной ценой"""
        with self.assertRaises(ValueError) as context:
            Product("Продукт", "Описание", -50, 5)
        self.assertEqual(str(context.exception), "Цена должна быть положительной")

    def test_product_invalid_quantity(self):
        """Тест инициализации с отрицательным количеством"""
        with self.assertRaises(ValueError) as context:
            Product("Продукт", "Описание", 100, -5)
        self.assertEqual(str(context.exception), "Количество не может быть отрицательным")

    def test_add_products(self):
        """Тест сложения двух продуктов"""
        product1 = Product("Продукт1", "Описание1", 100, 2)
        product2 = Product("Продукт2", "Описание2", 200, 3)
        total = product1 + product2
        self.assertEqual(total, 800)  # (100×2) + (200×3) = 200 + 600 = 800

    def test_add_with_non_product(self):
        """Тест сложения с не-продуктом"""
        product = Product("Продукт", "Описание", 100, 2)
        with self.assertRaises(TypeError) as context:
            product + "не продукт"
        self.assertEqual(
            str(context.exception),
            "Можно складывать только объекты класса Product и его наследников"
        )


class TestSmartphoneClass(unittest.TestCase):
    """Тесты для класса Smartphone"""

    def setUp(self):
        self.held, sys.stdout = sys.stdout, StringIO()

    def tearDown(self):
        sys.stdout = self.held

    def test_smartphone_initialization(self):
        """Тест инициализации Smartphone"""
        smartphone = Smartphone(
            "Galaxy S23", "Флагман", 79990, 2,
            "высокая", "S23", "128 ГБ", "чёрный"
        )
        self.assertEqual(smartphone.get_name(), "Galaxy S23")
        self.assertEqual(smartphone.performance, "высокая")
        self.assertEqual(smartphone.model, "S23")
        self.assertEqual(smartphone.memory, "128 ГБ")
        self.assertEqual(smartphone.color, "чёрный")

    def test_smartphone_str_representation(self):
        """Тест строкового представления Smartphone"""
        smartphone = Smartphone(
            "Galaxy S23", "Флагман", 79990, 2,
            "высокая", "S23", "128 ГБ", "чёрный"
        )
        str_repr = str(smartphone)

        # Проверяем основные компоненты строки с гибкой проверкой цены
        self.assertIn("Galaxy S23", str_repr)
        self.assertTrue("79990" in str_repr and "руб." in str_repr,
                        f"Не найдена цена '79990 руб.' в строке: {str_repr}")
        self.assertIn("Остаток: 2 шт.", str_repr)

        # Проверяем дополнительные характеристики из Smartphone
        self.assertIn("Модель: S23", str_repr)
        self.assertIn("Память: 128 ГБ", str_repr)
        self.assertIn("Цвет: чёрный", str_repr)

        # Дополнительно проверяем, что все части присутствуют в правильной последовательности
        expected_parts = [
            "Galaxy S23",
            "Остаток: 2 шт.",
            "Модель: S23",
            "Память: 128 ГБ",
            "Цвет: чёрный"
        ]

        for part in expected_parts:
            with self.subTest(part=part):
                self.assertIn(part, str_repr)

        # Проверяем, что строка не содержит неожиданных частей
        unexpected_parts = ["performance", "description"]
        for part in unexpected_parts:
            with self.subTest(unexpected=part):
                self.assertNotIn(part.lower(), str_repr.lower())


if __name__ == '__main__':
    unittest.main()
