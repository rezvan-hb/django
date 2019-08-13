from django.urls import path, re_path

from chat.views import conversation_view , ChatItem

urlpatterns = [
    re_path('chat/(?P<userparameter>\d{0,10})', conversation_view),
    path('chatitem/', ChatItem.as_view()),
]