
from django.urls import path, re_path
from users1.views import ListUsersItem , LoginItem , SignupItem , EditProfileItem , EmailVerification

urlpatterns = [
    # path('item/', views.users_list_item),
    path('item/', ListUsersItem.as_view()),
    path('user/Signup/', SignupItem.as_view()),
    path('user/Login/', LoginItem.as_view()),
    path('user/editprofile' , EditProfileItem.as_view()),
    re_path('user/verified/(?P<userparameter>[a-f0-9]{8}-[a-f0-9]{4}-[4][a-f0-9]{3}-[89aAbB][a-f0-9]{3}-[a-f0-9]{12})', EmailVerification.as_view())
]

