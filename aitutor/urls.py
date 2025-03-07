from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index_redirect, name='index'),
    path('home/', views.home, name='home'),
    path('admin/', admin.site.urls),
    path("lessons/", include("lessons.urls")),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("chatbot/", include('chatbot.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)