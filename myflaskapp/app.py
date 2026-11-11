"""Flask-додаток з маршрутизацією та JSON-ендпоінтом."""

from importlib.metadata import version
from flask import Flask, jsonify, request, url_for
from markupsafe import escape
from config import config_by_name


def create_app(config_name: str = "default") -> Flask:
    app = Flask(__name__)
    if config_name not in config_by_name:
        raise ValueError("Невідомий режим конфігурації")
    app.config.from_object(config_by_name[config_name])
    if config_name == "production" and not app.config.get("SECRET_KEY"):
        raise RuntimeError("Задайте FLASK_SECRET_KEY для production")
    register_routes(app)
    return app


def register_routes(app: Flask):
    @app.route("/")
    def index():
        return (
            '<!doctype html><html lang="uk"><meta charset="utf-8">'
            f'<link rel="stylesheet" href="{url_for("static", filename="style.css")}">'
            '<h1>Головна сторінка Flask</h1><p>Практична робота №5.</p>'
            '<a href="/about">Про додаток</a> | '
            '<a href="/api/info">API</a> | <a href="/greet">Привітання</a>'
            '</html>'
        )

    @app.route("/about")
    def about():
        return (
            '<!doctype html><html lang="uk"><meta charset="utf-8">'
            '<h1>Про Flask-додаток</h1>'
            '<p>Курс: Програмування Python</p><p>Практична робота №5</p>'
            '<p>Це приклад Application Factory.</p>'
            '<a href="/">На головну</a></html>'
        )

    @app.route("/api/info")
    def api_info():
        routes = sorted(rule.rule for rule in app.url_map.iter_rules())
        return jsonify({
            "framework": "Flask",
            "version": version("flask"),
            "debug": app.debug,
            "routes": routes,
        })

    @app.route("/greet")
    @app.route("/greet/<name>")
    def greet(name=None):
        name = name if name is not None else request.args.get("name", "Гість")
        return (
            '<!doctype html><html lang="uk"><meta charset="utf-8">'
            f'<h1>Привіт, {escape(name)}!</h1>'
            '<a href="/">На головну</a></html>'
        )


if __name__ == "__main__":
    application = create_app("development")
    application.run(debug=application.config["DEBUG"], port=5000)
