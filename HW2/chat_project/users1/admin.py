
from django.contrib import admin
from users1.models import Users,UserProfile
# Register your models here.

class UsersAdmin(admin.ModelAdmin):
    # fields = ( 'firstname', 'lastname' )
    list_display = ('firstname', 'lastname' , 'username' , 'password', 'token')
    search_fields = ('firstname', 'lastname' , 'username')

admin.site.register(Users, UsersAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    
    list_display = ('user','token')
    
admin.site.register(UserProfile, UserProfileAdmin)



