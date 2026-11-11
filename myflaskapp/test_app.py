"""Перевірка маршрутизації Flask."""

import unittest
from app import create_app


class FlaskRoutesTests(unittest.TestCase):
    def setUp(self):
        self.client = create_app("development").test_client()

    def test_index(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_about(self):
        self.assertEqual(self.client.get("/about").status_code, 200)

    def test_api(self):
        data = self.client.get("/api/info").get_json()
        self.assertEqual(data["framework"], "Flask")
        self.assertIn("/greet/<name>", data["routes"])

    def test_query_name(self):
        self.assertIn("Іван".encode(), self.client.get("/greet?name=Іван").data)

    def test_url_name(self):
        self.assertIn("Марія".encode(), self.client.get("/greet/Марія").data)

    def test_escaping(self):
        self.assertNotIn(b"<script>", self.client.get("/greet?name=<script>").data)


if __name__ == "__main__":
    unittest.main()
