from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, Book, Role, BorrowedBook
from .forms import BookForm  # Импортируем нашу форму

# Регистрируем модель User с кастомным админ-классом
admin.site.register(User)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookForm  # Используем кастомную форму
    list_display = ('title', 'author', 'published_date', 'isbn', 'added_by', 'borrowed_by', 'image_book')
    list_filter = ('author', 'published_date', 'added_by', 'borrowed_by')
    search_fields = ('title', 'author', 'isbn')
    date_hierarchy = 'published_date'

    def save_model(self, request, obj, form, change):
        # Проверяем поле added_by: если такого пользователя нет, устанавливаем None.
        if obj.added_by:
            try:
                User.objects.get(pk=obj.added_by.pk)
            except User.DoesNotExist:
                obj.added_by = None

        # Аналогично для поля borrowed_by.
        if obj.borrowed_by:
            try:
                User.objects.get(pk=obj.borrowed_by.pk)
            except User.DoesNotExist:
                obj.borrowed_by = None

        super().save_model(request, obj, form, change)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'event_type', 'start_date', 'location', 'organizer', 'max_participants', 'created_at', 'updated_at')
    list_filter = ('event_type', 'location', 'is_active', 'max_participants')
    search_fields = ('title', 'event_type', 'organizer')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(BorrowedBook)
class BorrowedBookAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrowed_date', 'returned_date', 'is_returned')
    list_filter = ('is_returned',)
    search_fields = ('user__name', 'book__title')
