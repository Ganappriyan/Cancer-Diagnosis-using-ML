from django.urls import path, include
from frontend.views import login, create_user

urlpatterns = [
    path('login/', login, name='login'),
    path('create-user/', create_user, name='create_user'),
]
