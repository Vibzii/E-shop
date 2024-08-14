from django.db import models


class Contact(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    contact_note = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


