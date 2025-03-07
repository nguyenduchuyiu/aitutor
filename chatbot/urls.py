from django.urls import path
from .views import chatbot_response, update_tab_context

urlpatterns = [
    path('api/get_response/', chatbot_response, name='chatbot-response'),
    path('api/tab_change/', update_tab_context, name='tab_change'),
] 