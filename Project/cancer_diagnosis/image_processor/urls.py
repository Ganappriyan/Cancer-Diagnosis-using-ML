from django.urls import path
from .views import process_image, history

urlpatterns = [
    path('', process_image, name='process_image'),
    path('history/', history, name='history')
]
