from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'test/', include('haystack.urls')),
    url(r'example/', 'Search.views.example_input', name='example'),  # 简单的信息接受示例
    url(r'form/', views.form, name='form'),
    url(r'game/', views.post_game, name='post game'),
]