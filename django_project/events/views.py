from django.contrib import messages
from django.shortcuts import redirect, render
from .data import EVENTS
from .forms import RegistrationForm


def home(request):
    return render(request, "events/home.html", {
        "heading": "Афіша студентських подій",
        "event_count": len(EVENTS),
        "events": EVENTS,
    })


def event_list(request):
    return render(request, "events/list.html", {
        "heading": "Усі події",
        "event_count": len(EVENTS),
        "events": EVENTS,
    })


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, "Заявку успішно перевірено та прийнято!")
            return redirect("home")
    else:
        form = RegistrationForm(initial={"event": request.GET.get("event", "")})
    return render(request, "events/register.html", {
        "form": form,
        "heading": "Реєстрація на подію",
        "event_count": len(EVENTS),
        "events": EVENTS,
    })
