import json


def load_data_from_json(filename: str = "data/products.json") -> list:
    """Загружает данные из JSON‑файла и
        создаёт объекты классов Product и Category."""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Отладочная печать — поможет увидеть структуру файла
        print("Загруженные данные (первые 200 символов):")
        if len(str(data)) > 200:
            print(str(data)[:200] + "...")
        else:
            print(data)
        print(f"Тип данных: {type(data)}")

        from main import Product, Category

        categories = []

        # Обрабатываем данные в зависимости от их структуры
        if isinstance(data, dict) and 'categories' in data:
            # Старый формат: { "categories": [...] }
            category_list = data['categories']
        elif isinstance(data, list):
            # Новый формат: [ { ... }, { ... } ] — массив категорий
            category_list = data
        else:
            print("Ошибка: неожиданный формат JSON. Ожидался массив категорий "
                  "или объект с ключом 'categories'.")
            return []

        for category_data in category_list:
            # Проверяем наличие обязательных полей категории
            required_category_fields = ['name', 'description', 'products']
            has_all_required_fields = all(
                key in category_data for key in required_category_fields
            )

            if not has_all_required_fields:
                print(f"Пропускаем категорию — отсутствуют "
                      f"обязательные поля: {category_data}")

                continue

            products = []
            for product_data in category_data['products']:
                # Проверяем наличие обязательных полей товара
                required_product_fields = [
                    'name',
                    'description',
                    'price',
                    'quantity'
                ]
                all_required_fields_present = all(
                    key in product_data for key in required_product_fields
                )

                if not all_required_fields_present:
                    print(f"Пропускаем товар — отсутствуют "
                          f"обязательные поля: {product_data}")
                    continue

                product = Product(
                    name=product_data['name'],
                    description=product_data['description'],
                    price=float(product_data['price']),
                    quantity=int(product_data['quantity'])
                )
                products.append(product)

            category = Category(
                name=category_data['name'],
                description=category_data['description'],
                products=products
            )
            categories.append(category)

        return categories

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден. Проверьте, что папка "
              "'data' существует и содержит файл 'products.json'.")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON‑файла: {e}")
        return []
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return []
