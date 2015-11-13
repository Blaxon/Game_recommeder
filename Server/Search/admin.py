from django.contrib import admin

# Register your models here.
from .models import GameInfo


class GameInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'theme', 'player_vote', 'time', 'score')


admin.site.register(GameInfo, GameInfoAdmin)