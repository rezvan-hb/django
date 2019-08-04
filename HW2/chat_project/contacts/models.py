from django.db import models

# Create your models here.

from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Users(models.Model):
    online = 'ON'
    busy = 'BU'
    away = 'AW'
    default = 'DF'
    contact_status = (
        ( online, "contact-status online"),
        ( busy, "contact-status busy"),
        ( away, "contact-status away"),
        ( default, "contact-status"),
    )
    classs = models.CharField( max_length = 2,
        choices=contact_status,
        default=default
        )
    src = models.URLField( max_length=250 , default = 'https://www.kasandbox.org/programming-images/creatures/Hopper-Cool.png' )

    alphanumeric = RegexValidator( r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    firstname = models.CharField( max_length = 100 , validators=[alphanumeric] )
    lastname = models.CharField( max_length = 100 , validators=[alphanumeric] )
    preview = models.CharField( max_length = 1000 , default = '' ) 

    def __str__(self):
        return self.firstname + " " + self.lastname

    
# class Messages(models.Model):
#     sent = 'S'
#     recive = 'R'
#     typee = ((sent,"sent") , (recive,"recive"))
#     message_type = models.CharField(max_length = 1,
#         choices=typee)
#     sender = models.ForeignKey( Contacts , on_delete = models.CASCADE, related_name='sss')
#     receiver = models.ForeignKey( Contacts , on_delete = models.CASCADE, related_name='sss2')
#     message = models.TextField()
#     date = models.DateTimeField(auto_now_add = True)

#     def __str__(self): 
#         return "%s -> %s : %s" %(self.sender.name, self.receiver.name, self.message)


class Conversations( models.Model ):
    name = models.CharField( max_length=100 )
    members = models.ManyToManyField( Users )
    is_group = models.BooleanField( )

    def __str__(self):
        return self.name


# class ConversationMembers(models.Model):
#     conversation_id = models.ForeignKey(
#         Conversations, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(
#         Users, on_delete=models.DO_NOTHING)
    
#     def __str__(self):
#         return "%s, %s" % (
#             self.conversation_id.name,
#             self.user_id.first_name
#         )

class Messages(models.Model):
    sender_id = models.ForeignKey(
        Users,
        on_delete = models.CASCADE)
    conversation_id = models.ForeignKey(
        Conversations,
        on_delete = models.CASCADE
    )
    text = models.TextField()
    date = models.DateField(null=True)

    def __str__(self):
        return "%s (%s): %s" % (
            self.sender_id.firstname, 
            self.conversation_id.name,
            self.text
        )
