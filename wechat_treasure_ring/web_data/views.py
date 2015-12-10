# -*- coding: utf-8 -*-
from django.http.response import HttpResponse, HttpResponseBadRequest
from wechat_response.models import *
import json
from django.views.decorators.csrf import csrf_exempt
from wechat_response.data import *


def ifregistered(request, openid):
    if RingUser.objects.filter(user_id=openid).exists():
        user = RingUser.objects.filter(user_id=openid)[0]
        user_info = {
            "ifregistered": True,
            "sex": user.sex,
            "age": user.age,
            "height": user.height,
            "weight": user.weight,
            "goal_step": user.target,
        }
        return HttpResponse(json.dumps(user_info))
    else:
        user_info = {"ifregistered": False}
        return HttpResponse(json.dumps(user_info))


@csrf_exempt
def register(request):
    user_sex = request.POST.get("sex")
    user_age = request.POST.get("age")
    user_height = request.POST.get("height")
    user_wight = request.POST.get("weight")
    user_goal = request.POST.get("goal_step")
    user_openid = request.POST.get("openid")
    print user_openid
    if RingUser.objects.filter(user_id=user_openid).exists():
        user = RingUser.objects.filter(user_id=user_openid)[0]
        user.sex = user_sex
        user.age=user_age
        user.height=user_height
        user.weight=user_wight
        user.target=user_goal
        user.save()
    else:
        user_new = RingUser(
            user_id=user_openid,
            sex=user_sex,
            age=user_age,
            height=user_height,
            weight=user_wight,
            target=user_goal,
            last_record=0,
            steps_totalused=0,
            headimgurl="none",
            nickname="none"
        )
        user_new.save()
        user_bird = BirdUser(
            openid=user_openid,
            steps_used=0,
            score_today=0,
            score_total=0
        )
        user_bird.save()
    return HttpResponse("add info successfully")


def game_rank(request):
    openid = request.GET.get("openid")
    game = request.GET.get("game")
    print openid
    print game
    if game == "bird":
        today_objects = BirdUser.objects.all().order_by('-score_today')
        total_objects = BirdUser.objects.all().order_by('-score_total')
    today_entries = get_partial_ranklist(openid, today_objects)
    total_entries = get_partial_ranklist(openid, total_objects)
    result = {
        "today": today_entries,
        "total": total_entries
    }
    return HttpResponse(json.dumps(result))


def get_partial_ranklist(openid, objects):
    l = objects.len()
    entries = []
    n = 0
    for item in objects:
        if item.openid == openid:
            break
        else:
            n += 1
    if n == 0:
        indexlist = [0, 1, 2, 3]
    elif n == l - 1 or n == l - 2:
        indexlist = [l - 4, l - 3, l - 2, l - 1]
    else:
        indexlist = [n - 1, n, n + 1, n + 2]
    if l <= 4:
        indexlist = range(l)
    for i in indexlist:
        entry_object = objects[i]
        entry = {
            "openid": entry_object.openid,
            "nickname": entry_object.nickname,
            "score": entry_object.score_today,
            "rank": i+1
        }
        entries.append(entry)
    return entries


def steps_info(request):
    openid = request.GET.get("openid")
    users = RingUser.objects.filter(user_id=openid)
    if len(users) == 0:
        return HttpResponse("no user")
    user = users[0]
    #获取该用户今天的总步数和已消耗步数
    steps_total = 100
    steps_left = steps_total - user.steps_totalused
    result = {
        "total": steps_total,
        "left": steps_left
    }
    return HttpResponse(json.dumps(result))


def start_game(request):
    openid = request.GET.get("openid")
    users = RingUser.objects.filter(user_id=openid)
    if len(users) == 0:
        return HttpResponse("no user")
    user = users[0]
    game = request.GET.get("game")
    if game == "bird":
        gameuser = BirdUser.objects.get(openid=openid)
        user.steps_totalused += 1000
        gameuser.steps_used += 1000
        user.save()
        gameuser.save()
    return HttpResponse("success")


def end_game(request):
    openid = request.GET.get("openid")
    game = request.GET.get("game")
    score = request.GET.get("score")
    if game == "bird":
        gameusers = BirdUser.objects.filter(openid=openid)
        if len(gameusers) == 0:
            return HttpResponse("no user")
        gameuser = gameusers[0]
        gameuser.score_today += score
        gameuser.score_total += score
        gameuser.save()
    return HttpResponse("success")


@csrf_exempt
def game_rank(request):
    game = request.GET.get('game')
    start = request.GET.get('start')
    end = request.GET.get('end')
    if game == "bird":
        results_today = BirdUser.objects.all().order_by('-score_today')[start:end]
        results_total = BirdUser.objects.all().order_by('-score_total')[start:end]
    ranklist_today = []
    ranklist_total = []
    for item in results_today:
        itemuser = RingUser.objects.get(user_id=item.openid)
        rankitem = {
            "openid":item.openid,
            "nickname":itemuser.nickname,
            "headimgurl":itemuser.headimgurl,
            "score":item.score_today
        }
        ranklist_today.append(rankitem)
    for item in results_total:
        itemuser = RingUser.objects.get(user_id=item.openid)
        rankitem = {
            "openid":item.openid,
            "nickname":itemuser.nickname,
            "headimgurl":itemuser.headimgurl,
            "score":item.score_total
        }
        ranklist_total.append(rankitem)
    result = {
        "today":ranklist_today,
        "total":ranklist_total
    }
    return HttpResponse(json.dumps(result))


def get_sleepdata(request):
    openid = request.GET.get("openid")
    data = access_sleeping(openid)
    return HttpResponse(json.dumps(data))


def get_sportsdata(request):
    openid = request.GET.get("openid")
    data = access_exercising(openid)
    return HttpResponse(json.dumps(data))

