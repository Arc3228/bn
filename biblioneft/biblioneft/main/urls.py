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
    path("books/", views.profile_view, name="books"),
    path("logout/", LogoutView.as_view(), name='logout'),
    path("chit-zal/", views.chit_zal, name='chit-zal'),
    path("office/", views.office, name='office'),
    path("lecktoriy/", views.lecktoriy, name='lecktoriy'),
    path("cafe/", views.cafe, name='cafe'),
    path("book_list/", views.book_list, name='book_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)