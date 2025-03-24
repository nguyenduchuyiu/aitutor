from django.urls import path
from .views import chatbot_response, update_tab_context

urlpatterns = [
    path('api/get_response/', chatbot_response, name='chatbot-response'),
    path('api/update_tab_context/', update_tab_context, name='update_tab_context'),
] 