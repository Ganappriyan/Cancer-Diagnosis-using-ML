from django.urls import path, include
from .views import home, process_image


urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('users_handler.urls')),
    path('process_image/', process_image, name='process_image'),
]
