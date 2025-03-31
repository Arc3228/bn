import os
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import LoginForm, RegistrationForm, BookForm, EventForm
from django.contrib import messages
from .models import Book, Event, BorrowedBook


def index(request):
    books = Book.objects.exclude(image_book__isnull=True).exclude(image_book__exact='')
    events = Event.objects.filter(is_active=True).order_by('start_date')
    return render(request, 'main/index.html', {'books': books, 'events': events})


def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user  # Автоматически назначаем организатором текущего пользователя
            event.save()
            form.save_m2m()
            return redirect('profile')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'event_form': form})


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data["phone"]
            password = form.cleaned_data["password"]
            user = authenticate(request, phone=phone, password=password)
            if user:
                login(request, user)
                return redirect("profile")
            else:
                messages.error(request, "Неверный телефон или пароль")
    else:
        form = LoginForm()
    return render(request, "auth/login.html", {"form": form})


def registration_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.username = form.cleaned_data['phone']
            user.save()
            login(request, user)
            return redirect("profile")
    else:
        form = RegistrationForm()
    return render(request, "auth/registration.html", {"form": form})


@login_required
def profile_view(request):
    book_form = BookForm()
    event_form = EventForm()
    borrowed_books = Book.objects.filter(borrowed_by=request.user)
    reserved_books = BorrowedBook.objects.filter(user=request.user, is_returned=False)
    registered_events = request.user.events_participated.all()  # События, на которые пользователь записан

    return render(request, "auth/profile.html", {
        "user": request.user,
        "form": book_form,
        "event_form": event_form,
        "borrowed_books": borrowed_books,
        "reserved_books": reserved_books,
        "registered_events": registered_events,
    })


@login_required
def add_book_view(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book_folder = generate_book_folder(book.title, book.author)
            book.image_book.field.upload_to = os.path.join('book', book_folder)
            book.added_by = request.user
            book.save()
            return redirect('profile')
        else:
            return render(request, "auth/profile.html", {"user": request.user, 'form': form})
    else:
        return redirect('profile')


def generate_book_folder(title, author):
    title = "".join(x for x in title if x.isalnum())
    author = "".join(x for x in author if x.isalnum())
    return f"{title}_{author}"


def chit_zal(request):
    return render(request, 'pages/chit-zal.html')


def office(request):
    return render(request, 'pages/office.html')


def lecktoriy(request):
    return render(request, 'pages/lecktoriy.html')


def cafe(request):
    return render(request, 'pages/cafe.html')


def book_list(request):
    books = Book.objects.exclude(image_book__isnull=True).exclude(image_book__exact='')
    return render(request, 'pages/book_list.html', {'books': books})


def search(request):
    query = request.GET.get('q', '').strip()
    book_results = Book.objects.filter(
        Q(title__icontains=query) | Q(author__icontains=query)
    ) if query else Book.objects.none()

    event_results = Event.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query)
    ) if query else Event.objects.none()

    context = {
        'query': query,
        'book_results': book_results,
        'event_results': event_results,
    }
    return render(request, 'main/search_results.html', context)


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'pages/book_detail.html', {'book': book})

@login_required
def reserve_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # Проверяем, не забронирована ли книга уже (если есть активная запись, где is_returned=False)
    if BorrowedBook.objects.filter(book=book, is_returned=False).exists():
        messages.error(request, "Эта книга уже забронирована")
    else:
        # Создаем новую запись о заимствовании книги
        BorrowedBook.objects.create(user=request.user, book=book)
        messages.success(request, "Книга успешно забронирована")
    # Рендерим страницу книги, чтобы сообщения были видны именно там
    return book_detail(request, pk)

@login_required
def return_book(request, pk):
    borrowed_book = get_object_or_404(BorrowedBook, pk=pk)
    if not borrowed_book.is_returned:  # Проверяем, не была ли уже возвращена книга
        borrowed_book.is_returned = True
        borrowed_book.returned_date = timezone.now()
        borrowed_book.save()
        messages.success(request, f"Книга '{borrowed_book.book.title}' возвращена.")
    else:
        messages.warning(request, "Эта книга уже была возвращена.")
    # Рендерим страницу книги, на которой произведено бронирование
    return book_detail(request, borrowed_book.book.pk)

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'pages/event_detail.html', {'event': event})

@login_required
def register_for_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    # Проверяем, не заполнено ли максимальное количество участников
    if event.max_participants and event.participants.count() >= event.max_participants:
        messages.error(request, "Извините, на это мероприятие уже нет мест.")
    elif event.participants.filter(id=request.user.id).exists():
        messages.info(request, "Вы уже зарегистрированы на это мероприятие.")
    else:
        event.participants.add(request.user)
        messages.success(request, f"Вы успешно зарегистрированы на мероприятие '{event.title}'.")
    # Вместо редиректа возвращаем отрендеренную страницу мероприятия
    return event_detail(request, pk)

@login_required
def cancel_event_registration(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if event.participants.filter(id=request.user.id).exists():
        event.participants.remove(request.user)
        messages.success(request, f"Вы успешно отменили регистрацию на мероприятие '{event.title}'.")
    else:
        messages.info(request, "Вы не зарегистрированы на это мероприятие.")
    # Рендерим страницу мероприятия, чтобы сообщения отображались только там
    return event_detail(request, pk)

def photo_obzor(request):
    return render(request, 'pages/photo_obzor.html')