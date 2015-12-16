from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/', views.register, name='register'),
    url(r'^addgame/', views.add_game, name='add game'),
    url(r'^updatetime/', views.update_time, name='update time'),
    url(r'^recommend/', views.game_recommend, name='game recommend'),
    url(r'^check/', views.check, name='check'),
]