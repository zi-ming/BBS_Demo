#coding=utf8

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Article(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey("Category")
    brief = models.CharField(max_length=255,blank=True,null=True)
    content = models.TextField()
    author = models.ForeignKey("UserProfile")
    pub_date = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    priority = models.SmallIntegerField(default=1000)
    head_img = models.ImageField(upload_to="uploads")
    status_choice = (('draft',u'草稿'),
                     ('published', u'已发布'),
                     ('hidden', u'隐藏'),
                     )
    status = models.CharField(max_length=32,choices=status_choice, default="draft")

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey("Article")
    parent_comment = models.ForeignKey("self",related_name="child_comments",
                                       blank=True,null=True)
    comment_choice = ((0,u"评论"),
                      (1, u"点赞"),
                      )
    comment_type = models.SmallIntegerField(choices=comment_choice, default=0)
    user = models.ForeignKey("UserProfile")
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.comment_type == 0 and len(self.comment.strip())==0:
            raise ValidationError(u"评论不能为空")

    def __str__(self):
        return "%s, P:%s, %s, %s"%(self.article,
                                   self.parent_comment.id if self.parent_comment is not None
                                   else "Null", self.user, self.comment)

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    brief = models.CharField(max_length=255,blank=True,null=True)
    set_as_top_menu = models.BooleanField(default=False)
    position = models.SmallIntegerField()
    admin = models.ForeignKey("UserProfile")
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    signature = models.TextField(null=True,blank=True)
    head_img = models.ImageField(upload_to="uploads",null=True,blank=True)

    # for webchat
    friends = models.ManyToManyField("self", related_name="friends_userprofile", blank=True)


    def __str__(self):
        return self.name



