import unittest

from fastapi.testclient import TestClient
from app.main import app


class CatalogIntegrationTests(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_catalog_api_workflow(self):
        # 1. Check service health
        health = self.client.get("/health")
        self.assertEqual(health.status_code, 200)

        # 2. Get all products
        response = self.client.get("/products")
        self.assertEqual(response.status_code, 200)

        products = response.json()
        self.assertGreaterEqual(len(products), 3)

        # 3. Get one product
        product_id = products[0]["id"]

        product_response = self.client.get(
            f"/products/{product_id}"
        )

        self.assertEqual(
            product_response.status_code, 200
        )

        self.assertEqual(
            product_response.json()["id"],
            product_id
        )


if __name__ == "__main__":
    unittest.main()