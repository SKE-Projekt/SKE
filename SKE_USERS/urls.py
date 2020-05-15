from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views


urlpatterns = [
    path('login/', views.LoginView, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/send_inv/<int:id>', views.SendTokenView, name='send_inv'),
    path('tokens/', views.InvTokenView, name='tokens')
]
