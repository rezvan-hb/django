
from django.urls import path
from . import views

urlpatterns = [
    path('list/users/', views.user_list),
]
