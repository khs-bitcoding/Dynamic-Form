from django.urls import path
from app import views

urlpatterns = [
    path('<str:type>', views.home, name='home'),
]
