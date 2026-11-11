from django import forms
from .data import EVENT_TYPES


class RegistrationForm(forms.Form):
    name = forms.CharField(
        label="Ім'я та прізвище", min_length=2, max_length=60,
        error_messages={
            "required": "Вкажіть ім'я та прізвище.",
            "min_length": "Введіть хоча б 2 символи.",
            "max_length": "Максимум 60 символів.",
        },
        widget=forms.TextInput(attrs={"placeholder": "Олена Петренко"}),
    )
    email = forms.EmailField(
        label="Електронна пошта",
        error_messages={"required": "Вкажіть електронну пошту.", "invalid": "Вкажіть правильну адресу електронної пошти."},
        widget=forms.EmailInput(attrs={"placeholder": "example@gmail.com"}),
    )
    event = forms.ChoiceField(
        label="Подія", choices=[("", "Оберіть подію"), *EVENT_TYPES],
        error_messages={"required": "Оберіть подію.", "invalid_choice": "Оберіть подію зі списку."},
    )
    message = forms.CharField(
        label="Повідомлення", min_length=10, max_length=500,
        error_messages={
            "required": "Напишіть повідомлення.",
            "min_length": "Повідомлення повинно містити хоча б 10 символів.",
            "max_length": "Максимум 500 символів.",
        },
        widget=forms.Textarea(attrs={"rows": 5, "placeholder": "Чому ви хочете відвідати цю подію?"}),
    )

    def clean_message(self):
        message = self.cleaned_data["message"]
        if len(message.split()) < 5:
            raise forms.ValidationError("Повідомлення повинно містити не менше 5 слів.")
        return message
