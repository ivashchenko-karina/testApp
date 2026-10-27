import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import requests
from order_service import app

class TestOrderService(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    @patch('order_service.requests.get')
    def test_create_order_success(self, mock_get):
        """Тест успішного створення замовлення з використанням Mock HTTP-запиту"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Ноутбук", "price": 1000.0, "stock": 5}
        mock_get.return_value = mock_response

        payload = {"order_id": "order-2", "product_id": "P1", "quantity": 1}
        response = self.client.post('/orders', json=payload)

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["total_price"], 1000.0)
        self.assertEqual(data["status"], "Created")

    @patch('order_service.requests.get')
    def test_create_order_out_of_stock(self, mock_get):
        """Тест відмови, якщо товару немає в наявності (Негативний сценарій)"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "Навушники", "price": 150.0, "stock": 0}
        mock_get.return_value = mock_response

        payload = {"order_id": "order-3", "product_id": "P3", "quantity": 1}
        response = self.client.post('/orders', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Недостатньо товару", response.json()["detail"])

    @patch('order_service.requests.get')
    def test_catalog_service_unavailable(self, mock_get):
        """Тест обробки помилки при недоступності зовнішнього API"""
        # Використовуємо стандартний виняток бібліотеки requests
        mock_get.side_effect = requests.exceptions.RequestException("Connection Refused")

        payload = {"order_id": "order-4", "product_id": "P1", "quantity": 1}
        response = self.client.post('/orders', json=payload)

        self.assertEqual(response.status_code, 503)

if __name__ == '__main__':
    unittest.main()