from datetime import date
import re
from django import forms
from django.core.exceptions import ValidationError
from .models import User, Book, Event


class LoginForm(forms.Form):
    phone = forms.CharField(
        label="Телефон",
        max_length=18,
        widget=forms.TextInput(attrs={"placeholder": 'Номер телефона', "id": 'tel'})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": 'Введите пароль'})
    )


class ValidationError(Exception):
    pass


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"placeholder": "Введите пароль"})
    )
    password_confirm = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"placeholder": "Подтвердите пароль"})
    )

    class Meta:
        model = User
        fields = [
            "surname",
            "name",
            "lastname",
            "date_of_birth",
            "education",
            "prof",
            "study_work",
            "phone",
            "passport",
            "given",
        ]
        labels = {
            "surname": "Фамилия",
            "name": "Имя",
            "lastname": "Отчество",
            "date_of_birth": "Дата рождения",
            "education": "Образование",
            "prof": "Профессия",
            "study_work": "Место учебы/работы",
            "phone": "Телефон",
            "passport": "Паспорт",
            "given": "Кем выдан",
        }
        widgets = {
            "surname": forms.TextInput(attrs={
                "placeholder": "Введите фамилию",
                "required": True,
                "pattern": "[А-Яа-яЁё]+",
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "Введите имя",
                "required": True,
                "pattern": "[А-Яа-яЁё]+",
            }),
            "lastname": forms.TextInput(attrs={
                "placeholder": "Введите отчество",
                "pattern": "[А-Яа-яЁё]+",
            }),
            "date_of_birth": forms.DateInput(attrs={
                "placeholder": "дд.мм.гггг",
                "type": "date",
                "required": True,
                "max": date.today().strftime("%Y-%m-%d"),
            }),
            "education": forms.TextInput(attrs={
                "placeholder": "Введите образование",
                "pattern": "[А-Яа-яЁё]+",
                "required": True,
                "id": "id_edu"
            }),
            "prof": forms.TextInput(attrs={
                "placeholder": "Введите профессию",
                "pattern": "[А-Яа-яЁё]+",
                "required": True,
                "id": "id_prof"
            }),
            "study_work": forms.TextInput(attrs={
                "placeholder": "Введите место учебы/работы",
                "pattern": "[А-Яа-яЁё]+",
                "required": True,
                "id": "id_sw"
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Введите телефон",
                "required": True,
                'id': "tel",
            }),
            "passport": forms.TextInput(attrs={
                "placeholder": "Введите паспортные данные",
                "required": True,
                'id': "passport",
            }),
            "given": forms.TextInput(attrs={
                "placeholder": "Кем выдан паспорт",
                "pattern": "[А-Яа-яЁё ]+",
                "required": True,
                "id": "id_given"
            }),
        }

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if date_of_birth > date.today():
            raise ValidationError("Дата рождения не может быть в будущем.")
        return date_of_birth

    def clean_surname(self):
        surname = self.cleaned_data.get('surname')
        if not re.match(r'^[А-Яа-яЁё]+$', surname):
            raise ValidationError("Фамилия должна содержать только русские буквы.")
        return surname

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not re.match(r'^[А-Яа-яЁё]+$', name):
            raise ValidationError("Имя должно содержать только русские буквы.")
        return name

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if lastname and not re.match(r'^[А-Яа-яЁё\s]+$', lastname):  # Отчество может быть пустым
            raise ValidationError("Отчество должно содержать только русские буквы.")
        return lastname

    def clean_ed(self):
        ed = self.cleaned_data.get('education')
        if not re.match(r'^[А-Яа-яЁё]+$', ed):
            raise ValidationError("Данное поле должно содержать только русские буквы.")
        return ed

    def clean_prof(self):
        prof = self.cleaned_data.get('prof')
        if not re.match(r'^[А-Яа-яЁё]+$', prof):
            raise ValidationError("Данное поле должно содержать только русские буквы.")
        return prof

    def clean_sw(self):
        sw = self.cleaned_data.get('study_work')
        if not re.match(r'^[А-Яа-яЁё]+$', sw):
            raise ValidationError("Данное поле должно содержать только русские буквы.")
        return sw

    def clean_given(self):
        given = self.cleaned_data.get('given')
        if not re.match(r'^[А-Яа-яЁё\s]+$', given):
            raise ValidationError("Данное поле должно содержать только русские буквы.")
        return given

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают")
        return cleaned_data


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title',
            'author',
            'description',
            'published_date',
            'isbn',
            'pages',
            'added_by',
            'borrowed_by',
            'image_book',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            "title": forms.TextInput(attrs={
                "placeholder": "Введите название",
                "required": True,
                "pattern": "[А-Яа-яЁё]+",
            }),
            "author": forms.TextInput(attrs={
                "placeholder": "Введите автора",
                "required": True,
                "pattern": "[А-Яа-яЁё]+",
            }),
            "isbn": forms.TextInput(attrs={
                "placeholder": "Введите isbn",
            }),
            "pages": forms.TextInput(attrs={
                "placeholder": "Введите количество страниц",
            }),
            "published_date": forms.DateInput(attrs={
                "placeholder": "дд.мм.гггг",
                "type": "date",
                "required": True,
                "max": date.today().strftime("%Y-%m-%d"),
            })
        }
        labels = {
            'title': 'Название книги',
            'author': 'Автор',
            'description': 'Описание',
            'isbn': 'ISBN',
            'pages': 'Количество страниц',
        }

    def __init__(self, *args, **kwargs):
        # Если передан instance, проверяем, существуют ли связанные объекты.
        instance = kwargs.get('instance')
        if instance:
            if instance.added_by and not User.objects.filter(pk=instance.added_by.pk).exists():
                instance.added_by = None
            if instance.borrowed_by and not User.objects.filter(pk=instance.borrowed_by.pk).exists():
                instance.borrowed_by = None
        super().__init__(*args, **kwargs)

    def clean_added_by(self):
        added_by = self.cleaned_data.get('added_by')
        if not added_by or not User.objects.filter(pk=added_by.pk).exists():
            return None
        return added_by

    def clean_borrowed_by(self):
        borrowed_by = self.cleaned_data.get('borrowed_by')
        if not borrowed_by or not User.objects.filter(pk=borrowed_by.pk).exists():
            return None
        return borrowed_by

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('added_by') == '':
            cleaned_data['added_by'] = None
        if cleaned_data.get('borrowed_by') == '':
            cleaned_data['borrowed_by'] = None
        return cleaned_data


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title',
            'description',
            'event_type',
            'start_date',
            'location',
            'organizer',
            'participants',
            'max_participants',
            'is_active',
        ]
        widgets = {
            # HTML5-виджет для выбора даты и времени
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            # Текстовое поле с несколькими строками для описания
            'description': forms.Textarea(attrs={'rows': 4}),
            'title': forms.TextInput(attrs={'placeholder': 'Введите название'}),
            'location': forms.TextInput(attrs={'placeholder': 'Место проведения'})
        }
        labels = {
            'title': 'Название мероприятия',
            'description': 'Описание',
            'event_type': 'Тип мероприятия',
            'start_date': 'Дата и время начала',
            'location': 'Место проведения',
            'organizer': 'Организатор',
            'participants': 'Участники',
            'max_participants': 'Максимальное количество участников',
            'is_active': 'Активно',
        }
