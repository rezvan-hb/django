
from django.contrib import admin
from chat.models import Conversations , Messages

class ConversationsAdmin(admin.ModelAdmin):
    # fields = ( 'firstname', 'lastname' )
    list_display = ('name', 'is_group')
    search_fields = ['name']

admin.site.register(Conversations, ConversationsAdmin)

class  MessagesAdmin(admin.ModelAdmin):
    # fields = ( 'firstname', 'lastname' )
    list_display = ('conversation_id', 'sender_id' , 'text' , 'date')
    search_fields = ['text']

admin.site.register( Messages, MessagesAdmin)