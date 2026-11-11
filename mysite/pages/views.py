"""Три сторінки навчального сайту Django."""

from django.http import HttpResponse
from django.utils.html import format_html


def index(request):
    return HttpResponse(
        '<!doctype html><html lang="uk"><meta charset="utf-8">'
        '<h1>Головна сторінка Django</h1>'
        '<p>Це сайт для практичної роботи №5.</p>'
        '<ul><li>Маршрути</li><li>Налаштування</li><li>Перевірка сторінок</li></ul>'
        '<a href="/about/">Про проєкт</a> | <a href="/contact/">Контакти</a>'
        '</html>'
    )


def about(request):
    return HttpResponse(
        '<!doctype html><html lang="uk"><meta charset="utf-8">'
        '<h1>Про проєкт</h1><p>Курс: Програмування Python</p>'
        '<p>Практична робота №5</p>'
        '<p>Ім’я студента: [вкажіть своє ім’я]</p>'
        '<a href="/">На головну</a></html>'
    )


def contact(request):
    name = request.GET.get("name", "").strip()
    if name:
        content = format_html("<h1>Вітаємо, {}!</h1>", name)
    else:
        content = "<h1>Контактна сторінка</h1><p>Передайте ім’я через ?name=Іван</p>"
    return HttpResponse(
        '<!doctype html><html lang="uk"><meta charset="utf-8">'
        + str(content) + '<a href="/">На головну</a></html>'
    )
