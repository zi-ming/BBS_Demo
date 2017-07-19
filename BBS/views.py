#coding=utf8

from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from BBS import models
from BBS import form
from BBS import comment_handle
import json

categorys = models.Category.objects.filter(set_as_top_menu=True).order_by("position")

def BBS(request, category_id = None):
    """
    新闻主页数据请求（默认获取第一条新闻分类下的所有新闻）
    :param category_id: 要请求的新闻类别ID
    """
    if category_id is None:
        selected_category = categorys.first()
    else:
        selected_category = categorys.get(id=category_id)
    articles = models.Article.objects.filter(category_id = selected_category.id, status='published')
    return render(request, "BBS/index.html", {"categorys":categorys, "selected_category":selected_category,
                                            "articles":articles})

def bbs_login(request):
    """
    用户登陆处理
        * 如果用户登陆成功，则返回原来的页面（如果不存在原来页面，则返回新闻主页）
          否则停留在登录页面
    """
    if request.method == "POST":
        user = authenticate(
            username = request.POST.get('username'),
            password = request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            return HttpResponseRedirect( request.GET.get("next") or "/bbs/")

    return render(request, "base_login.html")

def bbs_logout(request):
    """
    用户注销处理
    """
    logout(request)
    # return HttpResponseRedirect('/bbs/login/')
    return HttpResponseRedirect("/bbs/")

def article_detail(request, id):
    """
    显示已发表的新闻详细信息
    :param request:
    :param id: 新闻ID
    :return:
    """
    article = models.Article.objects.get(id = id)
    comment_set = models.Comment.objects.filter(article_id=id, comment_type=0)
    cmt_html = comment_handle.build_tree(comment_set)

    return render(request, "BBS/article_detail.html",{"article":article,
                                                      "cmt_html": cmt_html
                                                      })

def comment_submit(request):
    """
    发表评论处理
    :param request:
    :return:
    """
    if request.method == "POST":
        cmt_obj = models.Comment(
            article_id = request.POST.get("article_id"),
            parent_comment_id = request.POST.get("parent_cmt_id"),
            comment_type = request.POST.get("cmt_type"),
            user_id = request.user.userprofile.id,
            comment = request.POST.get("cmt"),
        )
        cmt_obj.save()
    obj_sum = models.Comment.objects.filter(article_id=request.POST.get("article_id"),comment_type=request.POST.get("cmt_type")).count()
    return HttpResponse(obj_sum)

def get_comments(request, article_id):
    """
    获取评论
    :param request:
    :param article_id: 新闻ID
    :return:
    """
    comment_set = models.Comment.objects.filter(article_id=article_id, comment_type=0)
    cmt_html = comment_handle.build_tree(comment_set)
    return HttpResponse(cmt_html)

@login_required
def postArticle(request):
    """
    发帖处理
    :param request:
    :return:
    """
    if request.method == "GET":
        article_form = form.ArticlePostForm()
        return render(request, "BBS/post_article.html", {"article_form":article_form})
    elif request.method == "POST":
        article_form = form.ArticlePostForm(request.POST, request.FILES)
        try:
            article_form.is_valid()
            data = article_form.cleaned_data    # 必须先is_valid()才有该属性
            data['author'] = request.user.userprofile
            article_obj = models.Article(**data)
            article_obj.save()
            return HttpResponseRedirect("http://localhost:8000/bbs/")
        except Exception as ex:
            print(ex)
            return render(request, "BBS/post_article.html", {"article_form": article_form})

def uploadfile(request):
    """
    上传图片
    :param request:
    :return:
    """
    if request.method == "POST":
        file_obj = request.FILES.get("filename")
        if file_obj == None:
            return HttpResponse("404")
        else:
            with open("uploads/%s"%file_obj.name,"wb+") as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            return HttpResponse("OK")
    else:
        return render(request, "BBS/uploadFile.html")

def get_latest_article_count(request):
    """
    获取未读新闻数量
    :param request:
    :return:
    """
    current_article_id = request.GET.get("latest_article_id")
    latest_article_count = models.Article.objects.filter(id__gt=current_article_id).count()
    # latest_article_count = 100
    return HttpResponse(json.dumps({"latest_article_count":latest_article_count}))

