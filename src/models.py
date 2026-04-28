import logging


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = None
        # Используем сеттер для валидации при инициализации
        if price <= 0:
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self.price = price
        self.quantity = int(quantity)

    @property
    def price(self) -> float:
        """Геттер для получения цены товара."""
        return self.__price

    @price.setter
    def price(self, value: float):
        """Сеттер для установки цены товара с проверкой на корректность."""
        if value <= 0:
            logging.warning("Цена не должна быть нулевая или отрицательная")
            return

        if self.__price is not None and value < self.__price:
            user_input = input(f"Цена понижается с {self.__price} до {value}. Подтвердить? (y/n): ").strip().lower()
            if user_input == 'y':
                self.__price = float(value)
                logging.info("Цена успешно изменена.")
            else:
                logging.info("Изменение цены отменено.")
        else:
            self.__price = float(value)

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None) -> 'Product':
        """
        Класс-метод для создания объекта Product из словаря с данными.
        Если товар с таким же именем уже существует в списке existing_products,
        обновляет количество и цену (выбирает максимальную).

        Args:
            product_data (dict): Словарь с данными товара.
            existing_products (list): Список существующих товаров для проверки дубликатов.
                                         Если None, проверка не выполняется.

        Returns:
            Product: созданный или обновлённый объект класса Product.

        Raises:
            KeyError: если в словаре отсутствуют обязательные ключи.
            ValueError: если значения имеют неверный тип.
        """
        # Проверяем наличие всех обязательных ключей
        required_keys = {'name', 'description', 'price', 'quantity'}
        if not required_keys.issubset(product_data.keys()):
            missing = required_keys - set(product_data.keys())
            raise KeyError(f"Отсутствуют обязательные ключи: {missing}")

        # Если список существующих товаров не передан или пуст, создаём новый продукт
        if existing_products is None or not existing_products:
            return cls(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )

        # Ищем товар с таким же именем в существующем списке
        existing_product = None
        for product in existing_products:
            if product.name == product_data['name']:
                existing_product = product
                break

        if existing_product:
            # Обновляем количество: суммируем старое и новое
            new_quantity = existing_product.quantity + product_data['quantity']

            # Выбираем максимальную цену
            new_price = max(existing_product.price, product_data['price'])

            # Обновляем атрибуты существующего продукта
            existing_product.quantity = new_quantity
            existing_product.price = new_price

            # Обновляем описание, если оно отличается
            if product_data['description'] != existing_product.description:
                existing_product.description = product_data['description']

            return existing_product
        else:
            # Товар не найден — создаём новый
            return cls(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                quantity=product_data['quantity']
            )


class Category:
    # Класс‑атрибут: счётчик всех продуктов во всех категориях
    product_counter = 0

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = []

        if products is not None:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию и обновляет счётчики."""
        if isinstance(product, Product):
            self.__products.append(product)
            # Увеличиваем глобальный счётчик на 1
            Category.product_counter += 1
        else:
            raise TypeError("Можно добавлять только объекты класса Product")

    @property
    def products(self) -> str:
        """
        Геттер для списка товаров (возвращает строку в формате:
        "{name}, {price} руб. Остаток: {quantity} шт." для каждого товара,
        разделённую переносами строк. Если товаров нет, возвращает
        "В категории нет товаров."
        """
        if not self.__products:
            return "В категории нет товаров."

        product_lines = []
        for product in self.__products:
            line = f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            product_lines.append(line)
        return "\n".join(product_lines)

    def get_product_count(self) -> int:
        """Возвращает количество товаров в категории."""
        return len(self.__products)

    @classmethod
    def get_total_product_count(cls) -> int:
        """Возвращает общее количество продуктов во всех категориях."""
        return cls.product_counter
