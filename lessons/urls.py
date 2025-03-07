from django.urls import path
from .views import lesson_detail, api_lesson_detail


urlpatterns = [
    path("<int:lesson_id>/", lesson_detail, name="lesson_detail"),
    path("api/<int:lesson_id>/", api_lesson_detail, name="api_lesson_detail"),
]
