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

    def __str__(self) -> str:
        """
        Возвращает строковое представление товара в формате:
        "Название продукта, X руб. Остаток: X шт."
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        """
        Сложение товаров: суммирует стоимость (цена × количество) двух товаров.
        Разрешено только для объектов одного класса.

        Args:
            other (Product): другой товар для сложения.

        Returns:
            float: общая стоимость двух товаров.

        Raises:
            TypeError: если товары принадлежат к разным классам.
        """
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product и его наследников")

        if type(self) is not type(other):
            raise TypeError(
                f"Нельзя складывать товары разных типов: "
                f"{type(self).__name__} и {type(other).__name__}"
            )

        return self.price * self.quantity + other.price * other.quantity

    def apply_discount(self, discount_percent: float) -> None:
        """Применяет скидку к цене товара."""
        if 0 <= discount_percent <= 100:
            new_price = self.price * (1 - discount_percent / 100)
            self.price = new_price
        else:
            logging.warning("Процент скидки должен быть от 0 до 100")

    def is_in_stock(self) -> bool:
        """Проверяет, есть ли товар в наличии."""
        return self.quantity > 0


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: str, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def get_memory_in_gb(self) -> int:
        """Возвращает объём памяти в ГБ."""
        import re
        numbers = re.findall(r'\d+', self.memory)
        return int(numbers[0]) if numbers else 0

    def is_high_performance(self) -> bool:
        """Проверяет, является ли смартфон высокопроизводительным."""
        high_eff = ['высокая', 'high', 'premium', 'top']
        return any(word in self.efficiency.lower() for word in high_eff)

    def __str__(self) -> str:
        base_info = super().__str__()
        return (f"{base_info} | Модель: {self.model}, "
                f"Память: {self.memory}, Цвет: {self.color}, "
                f"Производительность: {self.efficiency}")


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def get_germination_days(self) -> tuple:
        """Извлекает минимальный и максимальный срок прорастания в днях."""
        import re
        numbers = re.findall(r'\d+', self.germination_period)
        if len(numbers) == 2:
            return int(numbers[0]), int(numbers[1])
        elif len(numbers) == 1:
            return int(numbers[0]), int(numbers[0])
        else:
            return 0, 0

    def is_fast_germinating(self) -> bool:
        """Проверяет, быстро ли прорастает трава (менее 10 дней)."""
        min_days, _ = self.get_germination_days()
        return min_days < 10

    def __str__(self) -> str:
        base_info = super().__str__()
        return (f"{base_info} | Страна: {self.country}, "
                f"Срок прорастания: {self.germination_period}, Цвет: {self.color}")


class Category:
    category_count = 0  # счётчик категорий
    product_count = 0  # счётчик всех продуктов во всех категориях

    def __init__(self, name: str, description: str, products: list = None):
        self.name = name
        self.description = description
        self.__products = []

        # Увеличиваем счётчик категорий при создании нового объекта
        Category.category_count += 1

        # Обрабатываем передачу продуктов при инициализации
        if products is not None:
            for product in products:
                self.add_product(product)  # Используем add_product для корректного учёта

    def get_product_objects(self):
        """Возвращает список объектов товаров в категории"""
        return self.__products

    def add_product(self, product) -> None:
        """
        Добавляет продукт в категорию и обновляет счётчики.

        Args:
            product (Product): объект товара для добавления.

        Raises:
            TypeError: если переданный объект не является экземпляром Product или его наследником.
        """
        if not isinstance(product, Product):
            raise TypeError(
                f"Можно добавлять только объекты класса Product или его наследников. "
                f"Переданный объект: {type(product).__name__}"
            )

        self.__products.append(product)
        Category.product_count += 1  # Корректное увеличение счётчика продуктов

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

    def get_total_quantity_in_stock(self) -> int:
        """
        Возвращает общее количество товаров на складе (сумма quantity всех продуктов в категории).
        """
        return sum(product.quantity for product in self.__products)

    @classmethod
    def get_total_product_count(cls) -> int:
        """Возвращает общее количество продуктов во всех категориях."""
        return cls.product_count

    def find_products_by_name(self, search_term: str) -> list:
        """Находит товары по части названия."""
        return [p for p in self.__products if search_term.lower() in p.name.lower()]

    def get_total_cost(self) -> float:
        """Возвращает общую стоимость всех товаров в категории (цена × количество)."""
        return sum(p.price * p.quantity for p in self.__products)

    def remove_product(self, product_name: str) -> bool:
        """
        Удаляет товар из категории по названию.

        Args:
            product_name (str): название товара для удаления.

        Returns:
            bool: True, если товар был найден и удалён, False — если не найден.
        """
        initial_count = len(self.__products)
        self.__products = [p for p in self.__products if p.name != product_name]
        removed_count = initial_count - len(self.__products)

        if removed_count > 0:
            # Обновляем глобальный счётчик
            Category.product_count -= removed_count
            return True
        return False

    def update_product_quantity(self, product_name: str, new_quantity: int) -> bool:
        """
        Обновляет количество товара в категории.

        Args:
            product_name (str): название товара.
            new_quantity (int): новое количество.

        Returns:
            bool: True, если товар найден и количество обновлено, False — если товар не найден.
        """
        for product in self.__products:
            if product.name == product_name:
                if new_quantity >= 0:
                    product.quantity = new_quantity
            else:
                logging.warning("Количество не может быть отрицательным")
            return True
        return False

    def get_products_by_availability(self, in_stock: bool = True) -> list:
        """
        Возвращает товары по наличию на складе.

        Args:
            in_stock (bool): если True — возвращает товары в наличии,
                              если False — товары с нулевым количеством.

        Returns:
            list: список подходящих товаров.
        """
        if in_stock:
            return [p for p in self.__products if p.is_in_stock()]
        else:
            return [p for p in self.__products if not p.is_in_stock()]

    def clear_empty_products(self) -> int:
        """
        Удаляет из категории все товары с нулевым количеством.

        Returns:
            int: количество удалённых товаров.
        """
        initial_count = len(self.__products)
        self.__products = [p for p in self.__products if p.quantity > 0]
        removed_count = initial_count - len(self.__products)

        # Обновляем глобальный счётчик
        Category.product_count -= removed_count
        return removed_count

    def apply_discount_to_all(self, discount_percent: float) -> None:
        """
        Применяет скидку ко всем товарам в категории.

        Args:
            discount_percent (float): процент скидки (0–100).
        """
        for product in self.__products:
            product.apply_discount(discount_percent)

    def get_average_price(self) -> float:
        """
        Возвращает среднюю цену товаров в категории.

        Returns:
            float: средняя цена или 0, если товаров нет.
        """
        if not self.__products:
            return 0.0
        total_price = sum(p.price for p in self.__products)
        return total_price / len(self.__products)

    def get_statistics(self) -> dict:
        """
        Возвращает статистику по категории.

        Returns:
            dict: словарь с статистикой:
                - total_products: общее количество товаров;
                - total_quantity: общее количество на складе;
                - total_cost: общая стоимость;
                - average_price: средняя цена;
                - in_stock_count: количество товаров в наличии;
                - out_of_stock_count: количество отсутствующих товаров.
        """
        in_stock = self.get_products_by_availability(in_stock=True)
        out_of_stock = self.get_products_by_availability(in_stock=False)

        return {
            "total_products": self.get_product_count(),
            "total_quantity": self.get_total_quantity_in_stock(),
            "total_cost": self.get_total_cost(),
            "average_price": self.get_average_price(),
            "in_stock_count": len(in_stock),
            "out_of_stock_count": len(out_of_stock)
        }

    def __str__(self) -> str:
        """
        Возвращает строковое представление категории в формате:
        "Название категории, количество продуктов: X шт."
        где X — общее количество товаров на складе (сумма quantity всех продуктов).
        """
        total_quantity = self.get_total_quantity_in_stock()
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __len__(self) -> int:
        """Позволяет использовать len() для получения количества товаров в категории."""
        return self.get_product_count()

    def __contains__(self, product_name: str) -> bool:
        """Позволяет использовать оператор 'in' для проверки наличия товара."""
        return any(p.name == product_name for p in self.__products)
