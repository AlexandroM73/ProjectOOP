from abc import ABC, abstractmethod


class CreationLoggerMixin:
    """
    Миксин для логирования создания объектов.
    Печатает в консоль информацию о классе и параметрах при создании объекта.
    """

    def __init__(self, *args, **kwargs):
        self._creation_args = args
        self._creation_kwargs = kwargs
        print(f"{self.__class__.__name__}({', '.join(repr(arg) for arg in args)})")

        # Безопасный вызов родительского __init__ без аргументов
        try:
            super().__init__()
        except TypeError:
            # Если родительский __init__ требует аргументов, пропускаем
            pass

    def __repr__(self) -> str:
        """
        Возвращает строковое представление объекта, которое можно использовать
        для его воссоздания (соответствует формату вывода в __init__).
        """
        # Получаем все атрибуты экземпляра, исключая служебные
        attrs = []
        for key, value in self.__dict__.items():
            if not key.startswith('_') or key in ['_name', '_description', '_price', '_quantity']:
                attrs.append(f"{key}={value!r}")

        return f"{self.__class__.__name__}({', '.join(attrs)})"


class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    @abstractmethod
    def get_name(self) -> str: pass

    @abstractmethod
    def get_description(self) -> str: pass

    @abstractmethod
    def get_price(self) -> float: pass

    @abstractmethod
    def get_quantity(self) -> int: pass

    @abstractmethod
    def __str__(self) -> str: pass

    @abstractmethod
    def __add__(self, other) -> float: pass


class Product(BaseProduct, CreationLoggerMixin):
    """Базовый класс продукта."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        # Сначала инициализируем базовый класс
        super().__init__(name, description, price, quantity)

        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")

        self._name = name
        self._description = description
        self._price = float(price)
        self._quantity = int(quantity)

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def get_price(self) -> float:
        return self._price

    def get_quantity(self) -> int:
        return self._quantity

    def __str__(self) -> str:
        return f"{self._name}, {self._price} руб. Остаток: {self._quantity} шт."

    def __add__(self, other) -> float:
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только объекты класса Product и его наследников")
        return (self._price * self._quantity) + (other._price * other._quantity)

    def __repr__(self) -> str:
        return (f"Product(name='{self._name}', description='{self._description}', "
                f"price={self._price}, quantity={self._quantity})")


class Smartphone(Product):
    """Класс смартфона."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 performance: str, model: str, memory: str, color: str):
        super().__init__(name, description, price, quantity)
        self.performance = performance
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self) -> str:
        base_info = super().__str__()
        return f"{base_info} | Модель: {self.model} | Память: {self.memory} | Цвет: {self.color}"

    def __repr__(self) -> str:
        return (f"Smartphone(name='{self._name}', description='{self._description}', "
                f"price={self._price}, quantity={self._quantity}, "
                f"performance='{self.performance}', model='{self.model}', "
                f"memory='{self.memory}', color='{self.color}')")


class LawnGrass(Product):
    """Класс газонной травы."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self) -> str:
        base_info = super().__str__()
        return f"{base_info} | Страна: {self.country} | Всхожесть: {self.germination_period} | Цвет: {self.color}"

    def __repr__(self) -> str:
        return (f"LawnGrass(name='{self._name}', description='{self._description}', "
                f"price={self._price}, quantity={self._quantity}, "
                f"country='{self.country}', germination_period='{self.germination_period}', "
                f"color='{self.color}')")


# Абстрактный базовый класс для общих свойств
class BaseEntity(ABC):
    """Абстрактный базовый класс для сущностей с именем и описанием."""

    @abstractmethod
    def get_name(self) -> str:
        """Возвращает название сущности."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Возвращает описание сущности."""
        pass


# Класс категории
class Category(BaseEntity):
    """Класс категории товаров."""

    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def __str__(self) -> str:
        return f"Категория: {self._name} — {self._description}"


# Класс заказа
class Order(BaseEntity):
    """Класс заказа."""

    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Количество в заказе должно быть положительным")
        if product.get_quantity() < quantity:
            raise ValueError("Недостаточно товара на складе")

        self._product = product
        self._quantity = quantity
        self._total_price = product.get_price() * quantity

    def get_name(self) -> str:
        return self._product.get_name()

    def get_description(self) -> str:
        return self._product.get_description()

    def get_product(self) -> Product:
        """Возвращает товар, на который сделан заказ."""
        return self._product

    def get_quantity(self) -> int:
        """Возвращает количество товара в заказе."""
        return self._quantity

    def get_total_price(self) -> float:
        """Возвращает итоговую стоимость заказа."""
        return self._total_price

    def __str__(self) -> str:
        return (f"Заказ: {self.get_name()} | "
                f"Количество: {self._quantity} шт. | "
                f"Итого: {self._total_price} руб.")

    def __repr__(self) -> str:
        return (f"Order(product={repr(self._product)}, "
                f"quantity={self._quantity})")
