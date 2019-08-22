
from django.urls import path
from users1.views import ListUsersItem , LoginItem , SignupItem , EditProfileItem

urlpatterns = [
    # path('item/', views.users_list_item),
    path('item/', ListUsersItem.as_view()),
    path('user/Signup/', SignupItem.as_view()),
    path('user/Login/', LoginItem.as_view()),
    path('user/editprofile' , EditProfileItem.as_view()) 
]

