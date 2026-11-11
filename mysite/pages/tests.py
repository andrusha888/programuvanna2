"""Прості перевірки маршрутів Django."""

from django.test import SimpleTestCase


class PagesTests(SimpleTestCase):
    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Головна сторінка")

    def test_about(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)

    def test_contact(self):
        response = self.client.get("/contact/", {"name": "Іван"})
        self.assertContains(response, "Іван")

    def test_contact_escaping(self):
        response = self.client.get("/contact/", {"name": "<script>"})
        self.assertNotContains(response, "<script>")
