from django.db import models

class Contact(models.Model):
    title = models.CharField(max_length=50)
    text = models.CharField(max_length=500)
    email = models.EmailField()
    is_read = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=True)
