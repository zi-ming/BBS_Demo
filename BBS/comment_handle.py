#coding=utf8

from BBS import models

def build_tree(cmt_set=None):
    """
    生成树形评论
    :param cmt_set: 评论集合
    :return:
    """
    print("===>%s" % ([item.comment_type for item in cmt_set]))
    if cmt_set == None:
        cmt_set = models.Comment.objects.filter(article_id=1, comment_type=0)
    res_set = fun(cmt_set)
    html = convert_html(res_set)
    return html

def fun(cmt_set, pid=None):
    """
    递归遍历所有父评论下的子评论
    :param cmt_set: 父评论集合
    :param pid: 父评论ID
    :return:
    """
    parents = cmt_set.filter(parent_comment_id = pid)
    res = {}
    for parent in parents:
        childs = fun(cmt_set, parent.id)
        res[parent.id] = childs
    return res

def convert_html(cmt_set):
    """
    根据评集合生成对应的Html代码
    :param cmt_set: 评论集合
    :return: html字符串
    """
    html = ""
    for parent_id in cmt_set:
        cmt = models.Comment.objects.get(id=parent_id)

        cmt_btn = '<span cmt_id='+str(cmt.id)+' class="glyphicon glyphicon-comment cmt-margin" style="float:right;" aria-hidden="true"></span>'

        tmp_html = "<li>[%s] %s: %s %s</li>"%(cmt.id, cmt.user, cmt.comment, cmt_btn)
        html += tmp_html
        html += convert_html(cmt_set[parent_id])
    html = "<ul>%s</ul>"%html
    return html

