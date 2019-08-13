
from django.contrib import admin
from users1.models import Users
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    # fields = ( 'firstname', 'lastname' )
    list_display = ('firstname', 'lastname' , 'username' , 'password')
    search_fields = ('firstname', 'lastname' , 'username')

admin.site.register(Users, UsersAdmin)
