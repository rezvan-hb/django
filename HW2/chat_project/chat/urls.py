from django.urls import path, re_path

from chat.views import   ConversationItem , ChatItem
# from chat.HW4.views import MessageView

urlpatterns = [
    # re_path('chat/(?P<userparameter>\d{0,10})', conversation_view),
    path('chat/conversation', ConversationItem.as_view()),
    path('chat/message', ChatItem.as_view())
]