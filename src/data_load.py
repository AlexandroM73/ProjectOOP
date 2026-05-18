import json
from .models import Product, Category


def load_data_from_json(filename: str = "data/products.json") -> list:
    """Загружает данные из JSON‑файла и создаёт объекты Product и Category."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        categories = []

        # Обработка старого формата (с ключом 'categories')
        if 'categories' in data:
            raw_categories = data['categories']
        else:
            # Новый формат — массив категорий
            raw_categories = data

        for cat_data in raw_categories:
            if all(key in cat_data for key in ['name', 'description', 'products']):
                products = []
                for prod_data in cat_data['products']:
                    if all(key in prod_data for key in ['name', 'price', 'quantity']):
                        products.append(Product(
                            prod_data['name'],
                            prod_data.get('description', ''),
                            prod_data['price'],
                            prod_data['quantity']
                        ))
                categories.append(Category(
                    cat_data['name'],
                    cat_data['description'],
                    products
                ))

        return categories

    except (FileNotFoundError, json.JSONDecodeError):
        return []
