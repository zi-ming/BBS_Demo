#coding=utf8

from django.conf.urls import url
from BBS import views

urlpatterns = [
    url(r'^$', views.BBS, name="home"),
    url(r'^category/(\d+)/$',views.BBS, name='index'),
    url(r'^login/$', views.bbs_login, name="login"),
    url(r'^logout/$', views.bbs_logout, name="logout"),
    url(r'^detail/(\d+)$', views.article_detail, name="article_detail"),
    url(r'^comment_submit/$', views.comment_submit, name="comment_submit"),
    url(r'^getComments/(\d+)$', views.get_comments, name="getComments"),
    url(r'^postarticle/$', views.postArticle, name="postarticle"),

    url(r'^uploadfile/$', views.uploadfile, name="uploadfile"),
    url(r'^get_latest_article_count/$', views.get_latest_article_count, name="get_latest_article_count"),

]
