import unittest
from unittest.mock import patch, Mock

from fastapi.testclient import TestClient
from app.main import app, orders


class OrderUnitTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        orders.clear()

    @patch("app.main.httpx.get")
    def test_create_order(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 1,
            "name": "Laptop",
            "price": 25000.0
        }

        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 2
            }
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["total_price"],
            50000.0
        )

    def test_invalid_quantity(self):
        response = self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 0
            }
        )

        self.assertEqual(response.status_code, 422)

    @patch("app.main.httpx.get")
    def test_catalog_product_not_found(self, mock_get):
        import httpx

        request = httpx.Request(
            "GET",
            "http://catalog/products/999"
        )

        error_response = httpx.Response(
            404,
            request=request
        )

        mock_get.side_effect = httpx.HTTPStatusError(
            "Not found",
            request=request,
            response=error_response
        )

        response = self.client.post(
            "/orders",
            json={
                "product_id": 999,
                "quantity": 1
            }
        )

        self.assertEqual(response.status_code, 404)

    def test_order_not_found(self):
        response = self.client.get("/orders/999")

        self.assertEqual(response.status_code, 404)

    def test_health(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()