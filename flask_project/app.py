import os
import secrets
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_wtf.csrf import CSRFProtect
from data import EVENTS
from forms import RegistrationForm

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or secrets.token_urlsafe(48)
csrf = CSRFProtect(app)


@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}


@app.get("/")
def home():
    return render_template("home.html", heading="Афіша студентських подій", event_count=len(EVENTS), events=EVENTS)


@app.get("/events/")
def event_list():
    return render_template("list.html", heading="Усі події", event_count=len(EVENTS), events=EVENTS)


@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Заявку успішно перевірено та прийнято!", "success")
        return redirect(url_for("home"))
    if request.method == "GET":
        chosen_event = request.args.get("event", "")
        if chosen_event in dict(form.event.choices):
            form.event.data = chosen_event
    return render_template("register.html", form=form, heading="Реєстрація на подію", event_count=len(EVENTS), events=EVENTS)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
