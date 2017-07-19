#coding=utf8

from django.shortcuts import render, HttpResponse
import json, time, queue
from webchat import models

GLOBAL_MSG_QUEUE={}

def dashboard(request):
    return render(request, "webchat/dashboard.html")

def putMsg(to_id, msg):
    """
    把信息放到相应的消息队列
    :param to_id: 要发送的对象ID
    :param msg: 信息内容
    :return:
    """
    if not GLOBAL_MSG_QUEUE.get(to_id):
        GLOBAL_MSG_QUEUE[to_id] = queue.Queue()
    GLOBAL_MSG_QUEUE[to_id].put(msg)


def send_msg(request):
    """
    发送消息
    :param request:
    :return:
    """
    if request.method == "POST":
        msg = request.POST.get("data")
        if msg:
            msg = json.loads(msg)
            msg["timestamp"] = time.time()
            to_id = int(msg["to"])
            from_id = int(msg["from"])
            if msg["type"] == "single":
                putMsg(to_id, msg)
            else:
                members = models.WebGroup.objects.get(id=to_id).members
                for member in members.select_related():
                    if member.id != from_id:
                        putMsg(member.id, msg)

    # print(GLOBAL_MSG_QUEUE)
    return HttpResponse("OK")

def get_news_msg(request):
    """
    获取消息队列中的消息
    :param request:
    :return:
    """
    user_id = request.user.userprofile.id
    new_msgs = []
    if user_id not in GLOBAL_MSG_QUEUE:
        GLOBAL_MSG_QUEUE[user_id] = queue.Queue()
    msg_q = GLOBAL_MSG_QUEUE[user_id]
    for i in range(msg_q.qsize()):
        new_msgs.append(GLOBAL_MSG_QUEUE[user_id].get())
    return HttpResponse(json.dumps(new_msgs))

