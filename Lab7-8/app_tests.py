import unittest
from app import app


class AppTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.get_data(as_text=True),
            "Hello world from app in Docker container."
        )

    def test_info(self):
        response = self.client.get("/info")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["lab"], 4)
        self.assertEqual(response.get_json()["variant"], 5)

    def test_echo_valid_json(self):
        data = {"product": "Laptop", "quantity": 2}
        response = self.client.post("/echo", json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["received"], data)
        self.assertEqual(
            response.get_json()["message"],
            "POST request received"
        )

    def test_echo_without_json(self):
        response = self.client.post("/echo", data="hello")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Send a JSON object"
        )

    def test_echo_json_list(self):
        response = self.client.post("/echo", json=["Laptop", 2])
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Send a JSON object"
        )


if __name__ == "__main__":
    unittest.main()