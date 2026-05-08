from src.data_load import load_data_from_json
from src.models import Category
import logging

# Настройка логирования для отображения предупреждений
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def main():
    print("Запуск демонстрационного кода...")

    # Загрузка данных
    categories = load_data_from_json("data/products.json")

    # Вывод результатов
    print("\n=== ИТОГОВЫЕ СЧЁТЧИКИ ===")
    print(f"Всего категорий: {len(categories)}")

    total_products = 0
    for category in categories:
        total_products += category.get_product_count()

    print(f"Всего товаров: {total_products}")
    print(f"Общий счётчик товаров во всех категориях: {Category.get_total_product_count()}")

    for i, category in enumerate(categories, 1):
        print("\n" + "=" * 50)
        print(f"ДЕМОНСТРАЦИЯ ФУНКЦИЙ ДЛЯ КАТЕГОРИИ {i}: {category.name}")
        print("=" * 50)
        print(f"Описание: {category.description}")

        # 1. Вывод товаров через геттер products
        print("\n--- ТОВАРЫ В КАТЕГОРИИ ---")
        print(category.products)

        # 2. Статистика по категории
        print("\n--- СТАТИСТИКА ПО КАТЕГОРИИ ---")
        stats = category.get_statistics()
        for key, value in stats.items():
            # Улучшаем читаемость ключей: заменяем подчёркивания на пробелы и делаем заглавные буквы
            readable_key = key.replace('_', ' ').title()
            print(f"{readable_key}: {value}")

        # 3. Средняя цена
        print(f"\nСредняя цена товара: {category.get_average_price():.2f} руб.")

        # 4. Общая стоимость категории
        print(f"Общая стоимость товаров: {category.get_total_cost():.2f} руб.")

        # 5. Поиск товаров по названию
        print("\n--- ПОИСК ТОВАРОВ ---")
        search_term = "Galaxy"  # Изменяем поисковый запрос на часть реального названия
        found_products = category.find_products_by_name(search_term)
        if found_products:
            print(f"Найдено товаров по запросу '{search_term}': {len(found_products)}")
            for product in found_products:
                print(f"- {product.name}")
        else:
            print(f"Товаров по запросу '{search_term}' не найдено")

        # 6. Товары в наличии и отсутствующие
        print("\n--- НАЛИЧИЕ ТОВАРОВ ---")
        in_stock = category.get_products_by_availability(in_stock=True)
        out_of_stock = category.get_products_by_availability(in_stock=False)

        print(f"В наличии: {len(in_stock)} товаров")
        print(f"Нет в наличии: {len(out_of_stock)} товаров")

        # 7. Демонстрация магических методов
        print("\n--- МАГИЧЕСКИЕ МЕТОДЫ ---")
        print(f"Количество товаров в категории (len): {len(category)}")
        if category.get_product_count() > 0:
            sample_product = category.get_product_objects()[0]  # Получаем объект товара
            sample_product_name = sample_product.name
        else:
            sample_product_name = "Неизвестный товар"
        is_in_category = sample_product_name in category
        print(f"Товар '{sample_product_name}' в категории (in): {is_in_category}")

        # 8. Применение скидки ко всем товарам
        print("\n--- ПРИМЕНЕНИЕ СКИДКИ ---")
        discount = 10  # 10% скидка
        print(f"Применяем скидку {discount}% ко всем товарам категории...")
        category.apply_discount_to_all(discount)
        print("Цены после скидки:")
        print(category.products)

        # 9. Очистка отсутствующих товаров
        print("\n--- ОЧИСТКА ОТСУТСТВУЮЩИХ ТОВАРОВ ---")
        removed_count = category.clear_empty_products()
        print(f"Удалено отсутствующих товаров: {removed_count}")
        print(f"Осталось товаров в категории: {len(category)}")

        # 10. Обновление количества товара
        print("\n--- ОБНОВЛЕНИЕ КОЛИЧЕСТВА ТОВАРА ---")
        if category.get_product_count() > 0:
            sample_product = category.get_product_objects()[0]
            print(f"Обновляем количество для товара '{sample_product.name}'")
            print(f"Было: {sample_product.quantity} шт.")
            category.update_product_quantity(sample_product.name, sample_product.quantity + 5)
            print(f"Стало: {sample_product.quantity} шт.")
        else:
            print("В категории нет товаров для обновления.")

        # 11. Удаление товара (для демонстрации)
        print("\n--- УДАЛЕНИЕ ТОВАРА ---")
        if category.get_product_count() > 0:
            product_to_remove = category.get_product_objects()[0].name
            print(f"Пытаемся удалить товар: {product_to_remove}")
            if category.remove_product(product_to_remove):
                print("Товар успешно удалён")
            else:
                print("Товар не найден для удаления")
            print(f"Осталось товаров в категории: {len(category)}")
        else:
            print("В категории нет товаров для удаления.")

    # Финальная проверка общего счётчика
    print("\n" + "=" * 50)
    print("ФИНАЛЬНАЯ ПРОВЕРКА ОБЩЕГО СЧЁТЧИКА ТОВАРОВ")
    print("=" * 50)
    print(f"Общий счётчик товаров во всех категориях: {Category.get_total_product_count()}")


if __name__ == "__main__":
    main()
