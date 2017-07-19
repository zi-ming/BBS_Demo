from django import template

register = template.Library()

@register.filter
def truncate_imgUrl(img_url):
    res = img_url.url.replace("uploads/","")
    print(res)
    return res

@register.simple_tag
def cal_cmt_fvr(article):
    query_set = article.comment_set.select_related()
    cmt_info = {
        "sum_cmt":query_set.filter(comment_type=0).count(),
        "sum_fvr": query_set.filter(comment_type=1).count(),
    }
    return cmt_info

@register.filter
def cal_fvr(article):
    pass