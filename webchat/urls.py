#coding=utf8

from django.conf.urls import url, include
from webchat import views
urlpatterns = [
    url(r'^$', views.dashboard, name="webchat"),
    url(r'^send_msg$', views.send_msg, name="send_msg"),
    url(r'^get_msg$', views.get_news_msg, name="get_msg"),
]
