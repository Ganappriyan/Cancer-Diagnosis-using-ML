from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('users_handler.urls')),
    path('process_image/', include('image_processor.urls')),
]
