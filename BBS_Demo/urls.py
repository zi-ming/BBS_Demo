#coding=utf8

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^bbs/', include("BBS.urls")),
    url(r'^webchat/', include("webchat.urls")),
]
