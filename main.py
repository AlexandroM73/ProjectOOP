from src.data_load import load_data_from_json


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


if __name__ == "__main__":
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    description = (
        "Смартфоны, как средство не только коммуникации, "
        "но и получения дополнительных функций для удобства жизни"
    )
    category1 = Category(
        "Смартфоны",
        description,
        [product1, product2, product3]
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(category1.category_count)
    print(category1.product_count)

    product4 = Product("55\" QLED 4K", "Фоновая подсветка", 123000.0, 7)
    category2 = Category("Телевизоры",
                         "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
                         [product4])

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)

    # Загружаем данные из JSON
    categories = load_data_from_json("data/products.json")

    # Выводим информацию о загруженных данных
    for category in categories:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")
        print(f"Количество товаров: {len(category.products)}")
        print("Товары:")
        for product in category.products:
            print(f"  - {product.name}: "
                  f"{product.price} руб., "
                  f"{product.quantity} шт."
                  )

    # Проверяем счётчики
    print("\n === ИТОГОВЫЕ СЧЁТЧИКИ ===")
    print(f"Всего категорий: {Category.category_count}")
    print(f"Всего товаров: {Category.product_count}")
