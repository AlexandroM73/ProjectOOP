import pytest
from src.models import Product, Category


class TestProduct:
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


class TestCategory:
    @pytest.fixture
    def setup_products(self):
        """Фикстура для создания тестовых продуктов."""
        return [
            Product("Смартфон 1", "Описание 1", 30000.0, 5),
            Product("Смартфон 2", "Описание 2", 40000.0, 3),
            Product("Смартфон 3", "Описание 3", 50000.0, 2)
        ]

    def test_category_initialization(self, setup_products):
        """Проверяет корректность инициализации объекта Category."""
        category = Category(
            "Смартфоны", "Категория смартфонов", setup_products
        )

        assert category.name == "Смартфоны"
        assert category.description == "Категория смартфонов"
        assert len(category.products) == 3
        assert isinstance(category.products, list)
        assert all(isinstance(p, Product) for p in category.products)

    def test_category_count_increases(self, setup_products):
        """Проверяет, что счётчик категорий
            увеличивается при создании новой категории."""
        initial_count = Category.category_count
        Category("Новая категория", "Описание", setup_products[:1])
        assert Category.category_count == initial_count + 1

    def test_product_count_increases_correctly(self, setup_products):
        """Проверяет, что счётчик товаров увеличивается
            на количество товаров в новой категории."""
        initial_product_count = Category.product_count
        num_products = len(setup_products)
        Category("Ещё одна категория", "Описание", setup_products)
        assert Category.product_count == initial_product_count + num_products

    def test_multiple_categories_count(self):
        """Проверяет подсчёт категорий и товаров
                при создании нескольких категорий."""
        Category.category_count = 0
        Category.product_count = 0

        products1 = [
            Product("Товар 1", "Описание 1", 1000.0, 5),
            Product("Товар 2", "Описание 2", 2000.0, 3)
        ]
        products2 = [
            Product("Товар 3", "Описание 3", 1500.0, 4),
            Product("Товар 4", "Описание 4", 2500.0, 2),
            Product("Товар 5", "Описание 5", 3000.0, 1)
        ]

        Category("Категория 1", "Описание 1", products1)
        Category("Категория 2", "Описание 2", products2)

        assert Category.category_count == 2
        assert Category.product_count == 5  # 2 + 3 товара

    def test_empty_category(self):
        """Проверяет создание категории без товаров."""
        initial_category_count = Category.category_count
        initial_product_count = Category.product_count

        empty_category = Category("Пустая категория", "Без товаров", [])

        assert Category.category_count == initial_category_count + 1
        assert Category.product_count == initial_product_count
        assert len(empty_category.products) == 0

    def test_single_product_category(self):
        """Проверяет категорию с одним товаром."""
        single_product = [Product("Единственный товар", "Описание", 1000.0, 1)]
        initial_product_count = Category.product_count

        single_category = Category(
            "Одиночный товар", "Одна позиция", single_product
        )

        assert Category.product_count == initial_product_count + 1
        assert len(single_category.products) == 1
