
from django.urls import path
from users1.views import ListUsersItem , LoginItem , SignupItem

urlpatterns = [
    # path('item/', views.users_list_item),
    path('item/', ListUsersItem.as_view()),
    path('item/Login/', LoginItem.as_view()),
    path('item/Signup/', SignupItem.as_view()),
]