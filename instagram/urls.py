from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('register/', views.register, name = 'register'),
    path('login/', views.user_login, name = 'log_in'),
    path('logout/', views.user_logout, name = 'log_out'),
    path('data/', views.data, name = 'data'),
]