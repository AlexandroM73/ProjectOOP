from src.data_load import load_data_from_json

def main():
    print("Запуск демонстрационного кода...")

    # Загрузка данных
    categories = load_data_from_json("data/products.json")

    # Вывод результатов
    print(f"\n === ИТОГОВЫЕ СЧЁТЧИКИ ===")
    print(f"Всего категорий: {len(categories)}")
    total_products = sum(len(cat.products) for cat in categories)
    print(f"Всего товаров: {total_products}")


    for category in categories:
        print(f"\nКатегория: {category.name}")
        print(f"Описание: {category.description}")
        for product in category.products:
            print(f"  - {product.name}: {product.price} руб. ({product.quantity} шт.)")


if __name__ == "__main__":
    main()


