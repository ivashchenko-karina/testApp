import unittest
import os

from fastapi.testclient import TestClient
from app.main import app, orders


class OrderIntegrationTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.catalog_url = os.getenv(
            "CATALOG_URL",
            "http://localhost:8001"
        )

        cls.client = TestClient(app)

    def setUp(self):
        orders.clear()

    def test_create_order_using_catalog(self):
        import httpx

        # Check that Catalog Service is available
        catalog_response = httpx.get(
            f"{self.catalog_url}/products/1",
            timeout=3.0
        )

        self.assertEqual(
            catalog_response.status_code,
            200
        )

        # Create order
        response = self.client.post(
            "/orders",
            json={
                "product_id": 1,
                "quantity": 2
            }
        )

        self.assertEqual(response.status_code, 201)

        order = response.json()

        self.assertEqual(order["product_id"], 1)
        self.assertEqual(order["quantity"], 2)
        self.assertEqual(order["total_price"], 50000.0)

        # Retrieve created order
        order_response = self.client.get(
            f"/orders/{order['id']}"
        )

        self.assertEqual(order_response.status_code, 200)

    def test_order_with_nonexistent_product(self):
        response = self.client.post(
            "/orders",
            json={
                "product_id": 999,
                "quantity": 1
            }
        )

        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()