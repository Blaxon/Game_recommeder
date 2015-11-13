from django.db import models

# Create your models here.
from django.db import models


class GameInfo(models.Model):
    name = models.TextField(primary_key=True)
    simple_intro = models.TextField()
    type = models.TextField()
    language = models.TextField()
    display = models.TextField()
    theme = models.TextField()
    company = models.TextField()
    time = models.TextField()
    tag = models.TextField()
    player_vote = models.TextField()
    score = models.FloatField()
    introduction = models.TextField()
    pircture = models.TextField()

