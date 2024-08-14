from django.db import models


class Question(models.Model):

    title = models.CharField(max_length=300)
    answer = models.TextField()
    sort_order = models.IntegerField()
    expanded = models.BooleanField(default=False)


    def __str__(self):
        return self.title


