from tkinter.font import names

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='home'),
    path("login/", views.login_view, name="login"),
    path("registration/", views.registration_view, name="registration"),
    path("profile/", views.profile_view, name="profile"),
    path('add_book/', views.add_book_view, name='add_book'),
    path('add-event/', views.add_event, name='add_event'),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("chit-zal/", views.chit_zal, name='chit-zal'),
    path("office/", views.office, name='office'),
    path("lecktoriy/", views.lecktoriy, name='lecktoriy'),
    path("cafe/", views.cafe, name='cafe'),
    path("book_list/", views.book_list, name='book_list'),
    path('search/', views.search, name='search'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/reserve/', views.reserve_book, name='reserve_book'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('return_book/<int:pk>/', views.return_book, name='return_book'),
    path('event/<int:pk>/register/', views.register_for_event, name='register_for_event'),
    path('event/<int:pk>/cancel/', views.cancel_event_registration, name='cancel_event_registration'),
    path('photo_obzor', views.photo_obzor, name='photo_obzor'),
    path('sign-up',views.sign_up, name='sign_up'),
    path('schedule', views.schedule, name='schedule'),
    path('playbill', views.playbill, name='playbill')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
