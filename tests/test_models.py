import unittest
from unittest.mock import patch
from src.models import Product, Category, Smartphone, LawnGrass


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

    def test_product_str_representation(self):
        """Проверяем строковое представление объекта Product."""
        expected = "Смартфон, 49999.99 руб. Остаток: 10 шт."
        self.assertEqual(str(self.product), expected)

    def test_product_str_zero_quantity(self):
        """Проверяем строковое представление при нулевом остатке."""
        product = Product("Ноутбук", "Игровой ноутбук", 89999.0, 0)
        expected = "Ноутбук, 89999.0 руб. Остаток: 0 шт."
        self.assertEqual(str(product), expected)

    def test_product_str_low_price(self):
        """Проверяем строковое представление с низкой ценой."""
        product = Product("Наушники", "Беспроводные наушники", 2999.5, 25)
        expected = "Наушники, 2999.5 руб. Остаток: 25 шт."
        self.assertEqual(str(product), expected)

    def test_product_add_basic(self):
        """Проверяем базовое сложение двух товаров."""
        product1 = Product("Смартфон", "Описание", 50000.0, 2)
        product2 = Product("Наушники", "Описание", 5000.0, 3)

        result = product1 + product2
        expected = (50000.0 * 2) + (5000.0 * 3)  # 100 000 + 15 000 = 115 000
        self.assertEqual(result, expected)

    def test_product_add_zero_quantity(self):
        """Проверяем сложение с товаром с нулевым количеством."""
        product1 = Product("Смартфон", "Описание", 50000.0, 0)
        product2 = Product("Ноутбук", "Описание", 100000.0, 2)

        result = product1 + product2
        expected = (50000.0 * 0) + (100000.0 * 2)  # 0 + 200 000 = 200 000
        self.assertEqual(result, expected)

    def test_product_add_same_product(self):
        """Проверяем сложение одинаковых товаров."""
        product1 = Product("Книга", "Художественная", 1000.0, 5)
        product2 = Product("Книга", "Научная", 2000.0, 3)

        result = product1 + product2
        expected = (1000.0 * 5) + (2000.0 * 3)  # 5 000 + 6 000 = 11 000
        self.assertEqual(result, expected)

    def test_product_add_with_low_price(self):
        """Проверяем сложение с товаром с очень низкой ценой."""
        product1 = Product("Товар 1", "Описание", 0.01, 10)
        product2 = Product("Товар 2", "Описание", 5000.0, 4)

        result = product1 + product2
        expected = (0.01 * 10) + (5000.0 * 4)  # 0.1 + 20 000 = 20 000.1
        self.assertEqual(result, expected)

    def test_product_add_invalid_type(self):
        """Проверяем обработку сложения с некорректным типом."""
        product = Product("Смартфон", "Описание", 50000.0, 2)

        with self.assertRaises(TypeError) as context:
            product + "не товар"

        self.assertIn("Можно складывать только объекты класса Product", str(context.exception))

    def test_add_same_class_products(self):
        """Тест сложения товаров одного класса (оба — Product)."""
        product1 = Product("Товар 1", "Описание", 1000.0, 2)
        product2 = Product("Товар 2", "Описание", 2000.0, 3)

        total_cost = product1 + product2
        expected_cost = (1000.0 * 2) + (2000.0 * 3)  # 2000 + 6000 = 8000
        self.assertEqual(total_cost, expected_cost)

    def test_add_different_class_products_raises_type_error(self):
        """Тест: сложение товаров разных классов вызывает TypeError."""
        smartphone = Smartphone(
            "Galaxy S23", "Флагман", 79990, 2,
            "высокая", "S23", "128 ГБ", "чёрный"
        )
        grass = LawnGrass(
            "Зелёная трава", "Газонная", 1500, 10,
            "Россия", "7–14 дней", "зелёный"
        )

        with self.assertRaises(TypeError) as context:
            _ = smartphone + grass

        self.assertIn(
            "Нельзя складывать товары разных типов",
            str(context.exception)
        )
        self.assertIn("Smartphone", str(context.exception))
        self.assertIn("LawnGrass", str(context.exception))

    def test_add_with_non_product_object_raises_type_error(self):
        """Тест: сложение с не‑продуктовым объектом вызывает TypeError."""
        with self.assertRaises(TypeError) as context:
            _ = self.product + "не товар"

        self.assertIn(
            "Можно складывать только объекты класса Product",
            str(context.exception)
        )

    def test_add_with_none_raises_type_error(self):
        """Тест: сложение с None вызывает TypeError."""
        with self.assertRaises(TypeError) as context:
            _ = self.product + None

        self.assertIn(
            "Можно складывать только объекты класса Product",
            str(context.exception)
        )


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

    def test_category_str_empty(self):
        """Проверяем строковое представление пустой категории."""
        category = Category("Электроника", "Все электронные товары")
        expected = "Электроника, количество продуктов: 0 шт."
        self.assertEqual(str(category), expected)

    def test_category_str_single_product(self):
        """Проверяем строковое представление категории с одним товаром."""
        category = Category("Смартфоны", "Мобильные устройства")
        product = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5)
        category.add_product(product)
        expected = "Смартфоны, количество продуктов: 5 шт."
        self.assertEqual(str(category), expected)

    def test_category_str_multiple_products(self):
        """Проверяем категорию с несколькими товарами."""
        category = Category("Ноутбуки", "Портативные компьютеры")
        product1 = Product("MacBook Pro 16", "M2 Pro, 1TB SSD", 250000.0, 3)
        product2 = Product("Dell XPS 13", "Intel i7, 512GB SSD", 150000.0, 2)
        category.add_product(product1)
        category.add_product(product2)
        expected = "Ноутбуки, количество продуктов: 5 шт."  # 3 + 2 = 5
        self.assertEqual(str(category), expected)

    def test_category_str_after_adding_products(self):
        """Проверяем, что строковое представление обновляется после добавления товаров."""
        category = Category("Книги", "Литературные произведения")

        # До добавления товаров
        self.assertEqual(str(category), "Книги, количество продуктов: 0 шт.")

        # Добавляем первый товар
        product1 = Product("1984", "Джордж Оруэлл", 599.0, 10)
        category.add_product(product1)
        self.assertEqual(str(category), "Книги, количество продуктов: 10 шт.")

        # Добавляем второй товар
        product2 = Product("Мастер и Маргарита", "Михаил Булгаков", 799.0, 8)
        category.add_product(product2)
        self.assertEqual(str(category), "Книги, количество продуктов: 18 шт.")  # 10 + 8 = 18

    def test_category_str_with_zero_quantity_products(self):
        """Проверяем категорию, где у товаров нулевой остаток."""
        category = Category("Распродажи", "Товары со скидками")
        product1 = Product("Мышь беспроводная", "Оптическая", 999.0, 0)
        product2 = Product("Клавиатура механическая", "RGB подсветка", 2999.0, 0)
        category.add_product(product1)
        category.add_product(product2)
        expected = "Распродажи, количество продуктов: 0 шт."  # 0 + 0 = 0
        self.assertEqual(str(category), expected)

    def test_add_valid_product_subclass(self):
        """Тест добавления корректного продукта — наследника Product."""
        category = Category("Смартфоны", "Мобильные устройства")
        smartphone = Smartphone(
            "Galaxy S23", "Флагман", 79990, 2,
            "высокая", "S23", "128 ГБ", "чёрный"
        )

        initial_count = category.get_product_count()
        category.add_product(smartphone)
        final_count = category.get_product_count()

        self.assertEqual(final_count, initial_count + 1)
        self.assertIn(smartphone, category._Category__products)

    def test_add_lawn_grass_to_category(self):
        """Тест добавления газонной травы (наследника Product) в категорию."""
        category = Category("Газонная трава", "Семена и трава")
        grass = LawnGrass(
            "Зелёная трава", "Газонная", 1500, 10,
            "Россия", "7–14 дней", "зелёный"
        )

        initial_count = category.get_product_count()
        category.add_product(grass)
        final_count = category.get_product_count()

        self.assertEqual(final_count, initial_count + 1)
        self.assertIn(grass, category._Category__products)

    def test_add_string_raises_type_error(self):
        """Тест: добавление строки вызывает TypeError."""
        category = Category("Электроника", "Устройства")

        with self.assertRaises(TypeError) as context:
            category.add_product("Не товар")

        self.assertIn(
            "Можно добавлять только объекты класса Product или его наследников",
            str(context.exception)
        )
        self.assertIn("str", str(context.exception))

    def test_add_integer_raises_type_error(self):
        """Тест: добавление числа вызывает TypeError."""
        category = Category("Электроника", "Устройства")

        with self.assertRaises(TypeError) as context:
            category.add_product(123)

        self.assertIn(
            "Можно добавлять только объекты класса Product или его наследников",
            str(context.exception)
        )
        self.assertIn("int", str(context.exception))

    def test_add_none_raises_type_error(self):
        """Тест: добавление None вызывает TypeError."""
        category = Category("Электроника", "Устройства")

        with self.assertRaises(TypeError) as context:
            category.add_product(None)

        self.assertIn(
            "Можно добавлять только объекты класса Product или его наследников",
            str(context.exception)
        )
        self.assertIn("NoneType", str(context.exception))

    def test_multiple_valid_additions(self):
        """Тест последовательного добавления разных наследников Product."""
        category = Category("Все товары", "Смешанная категория")

        smartphone = Smartphone(
            "Galaxy S23", "Флагман", 79990, 2,
            "высокая", "S23", "128 ГБ", "чёрный"
        )
        grass = LawnGrass(
            "Зелёная трава", "Газонная", 1500, 10,
            "Россия", "7–14 дней", "зелёный"
        )

        # Добавляем смартфон
        category.add_product(smartphone)
        # Добавляем газонную траву
        category.add_product(grass)

        self.assertEqual(category.get_product_count(), 2)
        self.assertIn(smartphone, category._Category__products)
        self.assertIn(grass, category._Category__products)

    def test_add_invalid_types_multiple(self):
        """Тест обработки нескольких некорректных типов подряд."""
        category = Category("Электроника", "Устройства")

        invalid_objects = ["текст", 123, None, [], {}]

        for obj in invalid_objects:
            with self.subTest(obj_type=type(obj).__name__):
                with self.assertRaises(TypeError) as context:
                    category.add_product(obj)
                self.assertIn(
                    "Можно добавлять только объекты класса Product или его наследников",
                    str(context.exception)
                )


if __name__ == '__main__':
    unittest.main()
