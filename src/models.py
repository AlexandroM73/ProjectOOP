class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = float(price)
        self.quantity = int(quantity)


class Category:
    # Атрибуты класса — общие для всех объектов
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        # Атрибуты объекта — уникальные для каждого экземпляра
        self.name = name
        self.description = description
        self.products = products

        # Автоматическое обновление атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)
