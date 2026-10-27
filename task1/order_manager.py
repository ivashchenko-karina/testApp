import json

class OrderManager:
    def __init__(self, storage_file="orders.json"):
        self.storage_file = storage_file
        self.orders = {}

    def add_order(self, order_id: str, items: list, customer_email: str) -> dict:
        """1. Функція додавання нового замовлення"""
        if order_id in self.orders:
            raise ValueError(f"Замовлення з ID '{order_id}' вже існує.")
        if not items:
            raise ValueError("Список товарів не може бути порожнім.")
        if "@" not in customer_email:
            raise ValueError("Некоректна адреса електронної пошти.")

        order = {
            "order_id": order_id,
            "items": items,  # Список словників: [{"name": "Laptop", "price": 1000, "qty": 1}]
            "customer_email": customer_email,
            "status": "New"
        }
        self.orders[order_id] = order
        return order

    def calculate_total(self, order_id: str) -> float:
        """2. Функція розрахунку загальної вартості замовлення"""
        if order_id not in self.orders:
            raise KeyError(f"Замовлення '{order_id}' не знайдено.")
        
        total = sum(item["price"] * item["qty"] for item in self.orders[order_id]["items"])
        return round(total, 2)

    def update_status(self, order_id: str, new_status: str) -> str:
        """3. Функція оновлення статусу замовлення"""
        valid_statuses = ["New", "Processing", "Shipped", "Delivered", "Cancelled"]
        if order_id not in self.orders:
            raise KeyError(f"Замовлення '{order_id}' не знайдено.")
        if new_status not in valid_statuses:
            raise ValueError(f"Недопустимий статус: {new_status}")
        
        self.orders[order_id]["status"] = new_status
        return self.orders[order_id]["status"]

    def find_orders_by_customer(self, customer_email: str) -> list:
        """4. Функція пошуку замовлень за email клієнта"""
        return [order for order in self.orders.values() if order["customer_email"] == customer_email]

    def save_to_file(self) -> str:
        """5. Функція збереження замовлень у JSON-файл"""
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(self.orders, f, ensure_ascii=False, indent=4)
        return self.storage_file

    def load_from_file(self) -> int:
        """6. Функція завантаження замовлень із JSON-файлу"""
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                self.orders = json.load(f)
            return len(self.orders)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {self.storage_file} не знайдено.")