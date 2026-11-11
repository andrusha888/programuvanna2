from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from data import EVENT_TYPES


class RegistrationForm(FlaskForm):
    name = StringField("Ім'я та прізвище", validators=[
        DataRequired(message="Вкажіть ім'я та прізвище."),
        Length(min=2, max=60, message="Ім'я повинно містити від 2 до 60 символів."),
    ], render_kw={"placeholder": "Олена Петренко"})
    email = EmailField("Електронна пошта", validators=[
        DataRequired(message="Вкажіть електронну пошту."),
        Email(message="Вкажіть правильну адресу електронної пошти."),
    ], render_kw={"placeholder": "example@gmail.com"})
    event = SelectField("Подія", choices=[("", "Оберіть подію"), *EVENT_TYPES], validators=[
        DataRequired(message="Оберіть подію."),
    ])
    message = TextAreaField("Повідомлення", validators=[
        DataRequired(message="Напишіть повідомлення."),
        Length(min=10, max=500, message="Повідомлення повинно містити від 10 до 500 символів."),
    ], render_kw={"rows": 5, "placeholder": "Чому ви хочете відвідати цю подію?"})

    def validate_message(self, field):
        if len(field.data.split()) < 5:
            raise ValidationError("Повідомлення повинно містити не менше 5 слів.")
