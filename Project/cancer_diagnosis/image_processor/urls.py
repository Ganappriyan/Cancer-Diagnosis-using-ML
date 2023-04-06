from django.urls import path
from .views import process_image, history, clear_history

urlpatterns = [
    path('', process_image, name='process_image'),
    path('history/', history, name='history'),
    path('clear_history/', clear_history, name='clear_history'),
]
