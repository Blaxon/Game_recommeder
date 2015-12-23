from django.db import models

# Create your models here.
from django.db import models


class GameInfo(models.Model):
    name = models.TextField(primary_key=True)
    simple_intro = models.TextField(null=True)
    type = models.TextField(null=True)
    language = models.TextField(null=True)
    display = models.TextField(null=True)
    theme = models.TextField(null=True)
    company = models.TextField(null=True)
    time = models.TextField(null=True)
    tag = models.TextField(null=True)
    player_vote = models.TextField(null=True)
    score = models.FloatField(null=True)
    introduction = models.TextField(null=True)
    picture = models.TextField(null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return '/search/game/?name=%s' % self.name