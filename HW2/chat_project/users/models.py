
from django.db import models
from django.core.validators import RegexValidator

# from django.core.validators import URLValidator
# src = models.TextField(validators=[URLValidator()])

# Create your models here.

class Contacts(models.Model):
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
    classs = models.CharField(max_length = 2,
        choices=contact_status,
        default=default
        )
    src = models.URLField(max_length=250 , default = 'https://www.kasandbox.org/programming-images/creatures/Hopper-Cool.png' )

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')
    name = models.CharField(max_length = 100 , validators=[alphanumeric])

    preview = models.CharField(max_length = 1000 , default = '') 

    def __str__(self):
        return self.name

    
class Messages(models.Model):
    sent = 'S'
    recive = 'R'
    typee = ((sent,"sent") , (recive,"recive"))
    message_type = models.CharField(max_length = 1,
        choices=typee)
    sender = models.ForeignKey( Contacts , on_delete = models.CASCADE, related_name='sss')
    receiver = models.ForeignKey( Contacts , on_delete = models.CASCADE, related_name='sss2')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self): 
        return "%s -> %s : %s" %(self.sender.name, self.receiver.name, self.message)
