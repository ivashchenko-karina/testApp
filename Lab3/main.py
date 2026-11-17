import os
from order_manager import OrderManager


def main():
    # У Docker дані будемо записувати в папку /data.
    # Поза Docker за замовчуванням використовується поточна папка.
    storage_file = os.environ.get("ORDERS_FILE", "orders.json")

    # Створюємо папку для файлу, якщо її ще немає.
    storage_dir = os.path.dirname(storage_file)
    if storage_dir:
        os.makedirs(storage_dir, exist_ok=True)

    manager = OrderManager(storage_file=storage_file)

    # Під час запуску намагаємося відновити збережені замовлення.
    try:
        count = manager.load_from_file()
        print(f"Завантажено замовлень: {count}")
    except FileNotFoundError:
        print("Збережених даних ще немає. Починаємо з порожнього списку.")

    while True:
        print("\n=== Замовлення товарів. Варіант 5 ===")
        print("1. Додати замовлення")
        print("2. Показати всі замовлення")
        print("3. Розрахувати суму замовлення")
        print("4. Змінити статус")
        print("5. Знайти замовлення за email")
        print("6. Зберегти у файл")
        print("7. Завантажити з файлу")
        print("0. Зберегти та вийти")

        choice = input("Оберіть дію: ").strip()

        try:
            if choice == "1":
                order_id = input("ID замовлення: ").strip()
                email = input("Email клієнта: ").strip()

                if not order_id:
                    raise ValueError("ID не може бути порожнім.")

                items = []

                while True:
                    name = input("Назва товару: ").strip()
                    price = float(input("Ціна: "))
                    qty = int(input("Кількість: "))

                    if not name:
                        raise ValueError("Назва товару не може бути порожньою.")
                    if price <= 0 or qty <= 0:
                        raise ValueError("Ціна та кількість повинні бути додатними.")

                    items.append({
                        "name": name,
                        "price": price,
                        "qty": qty
                    })

                    more = input("Додати ще товар? (y/n): ").strip().lower()
                    if more != "y":
                        break

                manager.add_order(order_id, items, email)
                print("Замовлення додано.")

            elif choice == "2":
                if not manager.orders:
                    print("Замовлень немає.")

                for order_id, order in manager.orders.items():
                    total = manager.calculate_total(order_id)
                    print(
                        f"{order_id} | {order['customer_email']} | "
                        f"{order['status']} | Сума: {total}"
                    )
                    for item in order["items"]:
                        print(
                            f"  {item['name']}: "
                            f"{item['price']} x {item['qty']}"
                        )

            elif choice == "3":
                order_id = input("ID замовлення: ").strip()
                print("Сума:", manager.calculate_total(order_id))

            elif choice == "4":
                order_id = input("ID замовлення: ").strip()
                print("Статуси: New, Processing, Shipped, Delivered, Cancelled")
                status = input("Новий статус: ").strip()
                result = manager.update_status(order_id, status)
                print("Поточний статус:", result)

            elif choice == "5":
                email = input("Email клієнта: ").strip()
                orders = manager.find_orders_by_customer(email)
                print(f"Знайдено замовлень: {len(orders)}")
                for order in orders:
                    print(order)

            elif choice == "6":
                print("Збережено:", manager.save_to_file())

            elif choice == "7":
                print("Завантажено замовлень:", manager.load_from_file())

            elif choice == "0":
                manager.save_to_file()
                print("Дані збережено. Роботу завершено.")
                break

            else:
                print("Невідомий пункт меню.")

        except (ValueError, KeyError, OSError) as error:
            print("Помилка:", error)


if __name__ == "__main__":
    main()