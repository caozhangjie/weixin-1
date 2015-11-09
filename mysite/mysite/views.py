# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from wechat_sdk import WechatBasic
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
from database_request import *
from wechat.models import *
from django.template.loader import get_template
from django.template import Context
from wechat_sdk.messages import (
    TextMessage, VoiceMessage, ImageMessage, VideoMessage, LinkMessage, LocationMessage, EventMessage
)


@csrf_exempt
def index(request):
# 下面这些变量均假设已由 Request 中提取完毕
    WECHAT_TOKEN = 'sheep94lion'
    AppID = ''
    AppSecret = ''
 
    # 实例化 WechatBasic
    wechat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    if request.method == "GET":
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if not wechat.check_signature(signature = signature, timestamp = timestamp, nonce = nonce):
            return HttpResponse("Verify failed")
        else:
            return HttpResponse(request.GET.get('echostr'), content_type="text/plain")
    else:
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        if False:#not wechat.check_signature(signature = signature, timestamp = timestamp, nonce = nonce):
            return HttpResponse("Verify failed")
        try:
            wechat.parse_data(data = request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')
        message = wechat.get_message()
        if isinstance(message, EventMessage):
            if message.type == 'click':
                if message.key == 'STEP_COUNT':
                    print 1
                    #steplist = get_data("step", "234")
                    print 3
                    #step = steplist[0][0]
                    #print step
                    print 2
                    stepi = Record.objects.get(user = u"jiji")
                    step = stepi.step
                    response = wechat.response_text(u'跑了' + str(step) + u'步咯')#里面的数字应由其他函数获取
                    return HttpResponse(response)
                if message.key == 'CHART':
                    response = wechat.response_news([{'title': 'sheep94lion', 'description':'handsome', 'picurl': 'http://t11.baidu.com/it/u=1102242709,380988438&fm=58', 'url': 'http://59.66.139.90/chart/' + message.source}])
                    return HttpResponse(response)
        response = wechat.response_text(u'sheep94lion')
        return HttpResponse(response)

@csrf_exempt
def chart(request, user):
    #print user
    WECHAT_TOKEN = 'sheep94lion'
    AppID = ''
    AppSecret = ''
 
    # 实例化 WechatBasic
    wechat = WechatBasic(
        token=WECHAT_TOKEN,
        appid=AppID,
        appsecret=AppSecret
    )
    t = get_template('index.html')
    html = t.render(Context({}))
    return HttpResponse(html)