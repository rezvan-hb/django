
from django.urls import path , re_path
from . import views

urlpatterns = [
    re_path('list/contacts/(?P<userparameter>\d{0,10})/', views.contacts_list),
]
