from django.db import models

# Create your models here.
from django.db import models


class User(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    games = models.TextField(null=True)
    times = models.TextField(null=True)

    def __str__(self):
        return self.username