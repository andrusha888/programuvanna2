from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DATA = urlencode({
    "name": "Олена Петренко",
    "email": "olena@example.com",
    "event": "python",
    "message": "Хочу більше дізнатися про роботу Python на практиці.",
}).encode("utf-8")

for name, url in (
    ("Django", "http://127.0.0.1:8000/register/"),
    ("Flask", "http://127.0.0.1:5000/register/"),
):
    request = Request(url, data=DATA, method="POST")
    try:
        with urlopen(request, timeout=5) as response:
            print(f"{name}: HTTP {response.status}")
    except HTTPError as error:
        print(f"{name}: HTTP {error.code} (відмова без CSRF-токена)")
    except URLError as error:
        print(f"{name}: сервер недоступний: {error.reason}")
