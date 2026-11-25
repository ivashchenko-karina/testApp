import unittest

from fastapi.testclient import TestClient
from app.main import app, products


class CatalogUnitTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_get_products(self):
        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json()), 0)

    def test_get_product_by_id(self):
        response = self.client.get("/products/1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Laptop")

    def test_product_not_found(self):
        response = self.client.get("/products/999")

        self.assertEqual(response.status_code, 404)

    def test_health(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["status"],
            "healthy"
        )

    def test_product_has_price(self):
        response = self.client.get("/products/1")

        self.assertIn("price", response.json())
        self.assertGreater(
            response.json()["price"], 0
        )


if __name__ == "__main__":
    unittest.main()