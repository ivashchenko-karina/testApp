from order_manager import OrderManager

def main():
    manager = OrderManager()
    print("=== Система управління замовленнями (Варіант 5) ===")
    
    # Приклад використання функцій
    try:
        manager.add_order("ORD-101", [{"name": "Телефон", "price": 500, "qty": 1}], "user@example.com")
        manager.add_order("ORD-102", [{"name": "Чохол", "price": 15, "qty": 2}], "user@example.com")
        
        print("\nСписок створених замовлень:")
        for order_id, data in manager.orders.items():
            print(f"- {order_id}: Сума = ${manager.calculate_total(order_id)}, Статус = {data['status']}")

        manager.update_status("ORD-101", "Shipped")
        print(f"\nНовий статус ORD-101: {manager.orders['ORD-101']['status']}")

        print(f"Пошук за поштою 'user@example.com': Знайдено {len(manager.find_orders_by_customer('user@example.com'))} замовлень.")

    except Exception as e:
        print(f"Помилка: {e}")

if __name__ == "__main__":
    main()