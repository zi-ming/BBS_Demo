#coding=utf8

from django.db import models
from BBS.models import UserProfile

class WebGroup(models.Model):
    name = models.CharField(max_length=64)
    brief = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(UserProfile)
    admins = models.ManyToManyField(UserProfile, related_name="group_admins", blank=True)
    members = models.ManyToManyField(UserProfile, related_name="group_members", blank=True)
    max_members = models.IntegerField(default=200)

    def __str__(self):
        return self.name

