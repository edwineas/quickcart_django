from django.urls import path
from .views import RegisterUserView

urlpatterns = [
    path('customer/', RegisterUserView.as_view(), name='register'),
]