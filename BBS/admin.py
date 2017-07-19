from django.contrib import admin
from BBS import models

class ArticleAdminModel(admin.ModelAdmin):
    list_display = ("title","category", "author", "pub_date", "last_modify", "priority","status")

class CommentAdminModel(admin.ModelAdmin):
    list_display = ("article","parent_comment","comment","comment_type","user","date")

class CategoryAdminModel(admin.ModelAdmin):
    list_display = ("name", "set_as_top_menu", "position", "admin")


admin.site.register(models.Article, ArticleAdminModel)
admin.site.register(models.Comment, CommentAdminModel)
admin.site.register(models.Category, CategoryAdminModel)
admin.site.register(models.UserProfile)
