import re
from django.test import Client, TestCase
from django.urls import reverse


class EventPagesTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_home_and_list(self):
        for url in (reverse("home"), reverse("event_list"), reverse("register")):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertContains(response, "Студентські події")

    def test_csrf_without_token_is_rejected(self):
        response = self.client.post(reverse("register"), self.valid_data())
        self.assertEqual(response.status_code, 403)

    def test_invalid_form_preserves_input(self):
        response = self.client.get(reverse("register"))
        token = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', response.content).group(1).decode()
        data = self.valid_data()
        data["csrfmiddlewaretoken"] = token
        data["message"] = "Занадто мало слів"
        response = self.client.post(reverse("register"), data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "не менше 5 слів")

    def test_invalid_with_token_and_successful_with_token(self):
        response = self.client.get(reverse("register"))
        token = re.search(rb'name="csrfmiddlewaretoken" value="([^"]+)"', response.content).group(1).decode()
        invalid = self.valid_data()
        invalid["csrfmiddlewaretoken"] = token
        invalid["message"] = "Мало слів у реченні"
        response = self.client.post(reverse("register"), invalid)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "не менше 5 слів")
        self.assertContains(response, "Олена Петренко")
        valid = self.valid_data()
        valid["csrfmiddlewaretoken"] = token
        response = self.client.post(reverse("register"), valid, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Заявку успішно перевірено")

    @staticmethod
    def valid_data():
        return {
            "name": "Олена Петренко",
            "email": "olena@example.com",
            "event": "python",
            "message": "Хочу більше дізнатися про роботу Python на практиці.",
        }
