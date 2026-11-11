import html
import re
import unittest
from app import app


class EventPagesTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def test_pages(self):
        for path in ("/", "/events/", "/register/"):
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Студентські події", response.get_data(as_text=True))

    def test_csrf_without_token_is_rejected(self):
        response = self.client.post("/register/", data=self.valid_data())
        self.assertEqual(response.status_code, 400)

    def test_invalid_and_success_with_token(self):
        response = self.client.get("/register/")
        csrf_token = html.unescape(re.search(r'name="csrf_token"[^>]*value="([^"]+)"', response.get_data(as_text=True)).group(1))
        invalid = self.valid_data()
        invalid.update(csrf_token=csrf_token, message="Замало слів")
        response = self.client.post("/register/", data=invalid)
        self.assertEqual(response.status_code, 200)
        self.assertIn("не менше 5 слів", response.get_data(as_text=True))
        self.assertIn("Олена Петренко", response.get_data(as_text=True))
        valid = self.valid_data()
        valid["csrf_token"] = csrf_token
        response = self.client.post("/register/", data=valid, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Заявку успішно перевірено", response.get_data(as_text=True))

    @staticmethod
    def valid_data():
        return {
            "name": "Олена Петренко",
            "email": "olena@example.com",
            "event": "python",
            "message": "Хочу більше дізнатися про роботу Python на практиці.",
        }


if __name__ == "__main__":
    unittest.main()
