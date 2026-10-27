import unittest
from unittest.mock import patch, mock_open
from order_manager import OrderManager

class TestOrderManager(unittest.TestCase):

    def setUp(self):
        self.manager = OrderManager(storage_file="test_orders.json")
        self.valid_items = [{"name": "Мишка", "price": 25.0, "qty": 2}]

    def test_add_order_success(self):
        """Позитивний тест додавання замовлення"""
        order = self.manager.add_order("ORD-001", self.valid_items, "test@mail.com")
        self.assertEqual(order["order_id"], "ORD-001")
        self.assertIn("ORD-001", self.manager.orders)

    def test_add_order_duplicate_raises_exception(self):
        """Перевірка виключення при спробі додати дублікат ID (Негативний сценарій)"""
        self.manager.add_order("ORD-001", self.valid_items, "test@mail.com")
        with self.assertRaises(ValueError):
            self.manager.add_order("ORD-001", self.valid_items, "test@mail.com")

    def test_add_order_invalid_email_raises_exception(self):
        """Перевірка помилки при некоректній адресі email"""
        with self.assertRaises(ValueError):
            self.manager.add_order("ORD-002", self.valid_items, "invalid_email")

    def test_calculate_total(self):
        """Тест розрахунку вартості замовлення"""
        self.manager.add_order("ORD-001", self.valid_items, "test@mail.com")
        total = self.manager.calculate_total("ORD-001")
        self.assertEqual(total, 50.0)

    def test_update_status_invalid_status(self):
        """Тест передачі невалідного статусу"""
        self.manager.add_order("ORD-001", self.valid_items, "test@mail.com")
        with self.assertRaises(ValueError):
            self.manager.update_status("ORD-001", "UnknownStatus")

    def test_save_to_file_with_mock(self):
        """Тестування збереження у файл з використанням mock_open (ізоляція I/O)"""
        self.manager.add_order("ORD-001", self.valid_items, "test@mail.com")
        
        m = mock_open()
        with patch("builtins.open", m):
            filename = self.manager.save_to_file()
            self.assertEqual(filename, "test_orders.json")
            m.assert_called_once_with("test_orders.json", "w", encoding="utf-8")

    def test_load_from_file_not_found_raises_exception(self):
        """Перевірка обробки відсутнього файлу"""
        with patch("builtins.open", side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                self.manager.load_from_file()

if __name__ == "__main__":
    unittest.main()