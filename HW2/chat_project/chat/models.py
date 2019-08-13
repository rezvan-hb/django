
from django.db import models
from users1.models import Users

class Conversations(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(Users)
    is_group = models.BooleanField()

    def __str__(self):
        return self.name

class Messages(models.Model):
    sender_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE)
    conversation_id = models.ForeignKey(
        Conversations,
        on_delete=models.CASCADE
        )
    text = models.TextField()
    date = models.DateField()

    def __str__(self):
        return "%s (%s): %s" % (
            self.sender_id.first_name, 
            self.conversation_id.name,
            self.text
        )

        