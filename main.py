from src.data_load import load_data_from_json


def main():
    print("Запуск демонстрационного кода...")

    # Загрузка данных
    categories = load_data_from_json("data/products.json")

    # Вывод результатов
    print("\n=== ИТОГОВЫЕ СЧЁТЧИКИ ===")
    print(f"Всего категорий: {len(categories)}")

    total_products = 0
    for category in categories:
        # Считаем количество товаров в категории через вспомогательный метод
        total_products += category.get_product_count()

    print(f"Всего товаров: {total_products}")

    for category in categories:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")

        # Используем геттер products — он возвращает строку с форматированным списком
        print("Товары:")
        print(category.products)  # Выводим готовую строку от геттера


if __name__ == "__main__":
    main()
