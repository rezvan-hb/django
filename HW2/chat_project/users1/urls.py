
from django.urls import path
from . import views

urlpatterns = [
    # path('item/', views.users_list_item),
    path('item/', views.ListUsersItem.as_view()),
    path('item/Login/', views.LoginItem.as_view()),
]