from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone field must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(phone, password, **extra_fields)


class Role(models.Model):
    ROLE_TYPES = [
        ('admin', 'Администратор'),
        ('bibliographer', 'Библиограф'),
        ('chief', 'Руководитель клубного формирования'),
        ('user', 'Пользователь'),
        ('guest', 'Гость'),
    ]

    name = models.CharField(max_length=50, choices=ROLE_TYPES, unique=True, verbose_name="Название роли")
    description = models.TextField(verbose_name="Описание роли", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = "Роль"
        verbose_name_plural = "Роли"


class User(AbstractBaseUser):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    education = models.CharField(max_length=100)
    prof = models.CharField(max_length=100)
    study_work = models.CharField(max_length=100)
    phone = models.CharField(max_length=18, unique=True)
    passport = models.CharField(max_length=11, unique=True)
    given = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Роль",
        related_name="users"
    )

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'surname', 'lastname', 'date_of_birth', 'education', 'prof', 'study_work', 'passport',
                       'given']

    objects = UserManager()

    def __str__(self):
        return f"{self.surname} {self.name}"

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    author = models.CharField(max_length=100, verbose_name="Автор")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    published_date = models.DateField(verbose_name="Дата написания")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    pages = models.PositiveIntegerField(verbose_name="Количество страниц", validators=[MinValueValidator(1)])

    borrowed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Взято на чтение",
        related_name="borrowed_books_by"
    )

    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Добавлено пользователем",
        related_name="added_books"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image_book = models.ImageField(upload_to='book/', blank=True, null=True)


    def __str__(self):
        return f"{self.title} by {self.author}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BorrowedBook(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Если пользователь удаляется, книги остаются
        verbose_name="Пользователь",
        related_name="borrowed_books_user"
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,  # Удалять запись о заимствовании, если книга удалена
        verbose_name="Книга",
        related_name="borrowed_books_book"
    )

    borrowed_date = models.DateTimeField(default=timezone.now, verbose_name="Дата взятия")
    returned_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата возврата")
    is_returned = models.BooleanField(default=False, verbose_name="Возвращена")

    def __str__(self):
        return f"{self.user} взял(а) книгу '{self.book}'"

    class Meta:
        verbose_name = "Взятая книга"
        verbose_name_plural = "Взятые книги"


class Event(models.Model):
    EVENT_TYPES = [
        ('concert', 'Концерт'),
        ('lecture', 'Лекция'),
        ('workshop', 'Мастер-класс'),
        ('meetup', 'Встреча'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=200, verbose_name="Название мероприятия")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, verbose_name="Тип мероприятия")
    start_date = models.DateTimeField(verbose_name="Дата и время начала")
    location = models.CharField(max_length=200, verbose_name="Место проведения")

    organizer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Если организатор удален, оставить событие
        null=True,
        blank=True,
        verbose_name="Организатор",
        related_name="organized_events"
    )

    participants = models.ManyToManyField(
        User,
        related_name="events_participated",
        blank=True,
        verbose_name="Зрители"
    )

    max_participants = models.PositiveIntegerField(
        verbose_name="Максимальное количество зрителей",
        validators=[MinValueValidator(1)],
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"{self.title} ({self.get_event_type_display()})"

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
