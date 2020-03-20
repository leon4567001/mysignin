#!/usr/bin/env python
# coding: utf-8
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone #引入timezone模块
from hr_signin.models import Event, People
from hr_signin.froms import AddEventForm, PeopleSingForm


# Create your views here.
def hello(request):
    """this is a test!"""
    return HttpResponse('hello,world!')

# 首页
def index(request):
    """返回渲染后的页面"""
    return render(request, "index.html")

# 登录操作
def login_action(request):
    """Form a complex number.
    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
    if request.method == "POST":
        login_username = request.POST.get("username")
        login_password = request.POST.get("password")
        if login_username == '' or login_password == '':
            return render(request, "index.html", {"error":"username or password null"})                 
        # else:
        user = auth.authenticate(username=login_username, password=login_password)
        if user is not None:
            auth.login(request, user) # 验证登录
            response = HttpResponseRedirect('/event_manage/') # 跳转到管理页面
            # response.set_cookie('user',login_username, 3600)
            request.session['user'] = login_username # 将 session 信息记录到浏览器
            return response
            # else:
        return render(request, "index.html", {"error":"username or password error"})
        # 跳转到index并传送 error 参数
    else:
        return render(request, "index.html")

# 活动管理页面
@login_required # 这个方法是需要登录的
def event_manage(request):
    '''
    获取session并查询所有event
    '''
    #username = request.COOKIES.get('user', '')  # 读取浏览器 cookie
    username = request.session.get('user', '') # 读取浏览器 session
    events = Event.objects.all()
    return render(request, "event_manage.html", {"user": username, "events": events})

# 根据活动名称搜索
@login_required
def search_name(request):
    username = request.session.get('user', '')
    searchname = request.GET.get("name", "")
    #search_name_bytes = search_name.encode(encoding="utf-8")
    events = Event.objects.filter(name__contains=searchname)
    if len(events) == 0:
        return render(request, "event_manage.html", {"user": username,
                                                     "hint": "没有找到该名称的活动！"})
    return render(request, "event_manage.html", {"user": username, "events": events})

# 添加活动
def add_event(request):
    username = request.session.get('user', '')

    if request.method == 'POST':
        form = AddEventForm(request.POST) # form 包含提交的数据
        if form.is_valid():
            name = form.cleaned_data['name']
            address = form.cleaned_data['address']
            detail = form.cleaned_data['detail']

            Event.objects.create(name=name, address=address, detail=detail)
            return render(request, "add_event.html", {"user": username, "form": form, "success": "添加活动成功!"})

    else:
        form = AddEventForm()

    return render(request, "add_event.html", {"user": username, "form": form})

# 人员管理
@login_required
def people_manage(request, event_id):
    username = request.session.get('user', '')
    print(event_id)
    # people_list = People.objects.get_queryset().order_by('id')
    people_list = People.objects.filter(event_id=event_id)

    paginator = Paginator(people_list, 10)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果页数不是整型, 取第一页.
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果页数超出查询范围，取最后一页
        contacts = paginator.page(paginator.num_pages)
    return render(request, "people_manage.html", {"user": username, "people_list": contacts})

# 根据姓名的查询
@login_required
def search_people(request):
    username = request.session.get('user', '')
    people_searched = request.GET.get("people", "")
    people_list = People.objects.filter(realname__contains=people_searched)

    if len(people_list) == 0:
        return render(request, "people_manage.html", {"user": username,
                                                     "hint": "查询结果为空！"})

    paginator = Paginator(people_list, 5)  #少于5条数据不够分页会产生警告
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request, "people_manage.html", {"user": username,
                                                 "people_list": contacts,
                                                 "people":people_searched})

# 开关签到
@login_required
def swich_action(request, event_id):
    username = request.session.get('user', '')
    events = Event.objects.all()
    # 查询目前的状态
    event = Event.objects.get(id=event_id)
    status_now = event.status
    print("当前状态为:" +str(status_now)) # 强制转换
    if status_now:
        # 关闭并记录关闭时间
        Event.objects.filter(id=event_id).update(status=0, end_time=datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M:%S'))
        # return render(request, "event_manage.html", {"user": username, "events": events})
    else:
        # 打开并记录打开时间
        Event.objects.filter(id=event_id).update(status=1, start_time=datetime.strftime(timezone.now(), '%Y-%m-%d %H:%M:%S'))
    
    return render(request, "event_manage.html", {"user": username, "events": events})

# 签到页面
def sign_index(request, event_id):
    # 查询活动名称传输到页面
    event = Event.objects.get(id=event_id)
    event_name = event.name
    print("-------"+event_name)
    # 接收form参数更新到数据库
    if request.method == 'POST':
        form = PeopleSingForm(request.POST)
        if form.is_valid():
            realname = form.cleaned_data['realname']
            empno = form.cleaned_data['empno']
            user_agent = form.cleaned_data['user_agent']
            # 检查user_agent是否存在
            # check_angent = People.objects.filter(user_agent=user_agent, event_id=event_id)
            # hint = "设备号重复,签到失败!"
            # if check_angent.count() == 0:
                # hint = "签到成功"
                # People.objects.create(realname=realname, empno=empno, event_id=event_id, user_agent=user_agent)
            # hint = "签到成功!"
            People.objects.create(realname=realname, empno=empno, event_id=event_id, user_agent=user_agent)
            # return render(request, "sign_index.html", {"form": form, "success": hint, "event_name": event_name})
            return render(request, 'success.html')
    else:
        form = PeopleSingForm()

    return render(request, "sign_index.html", {"form": form, "event_name": event_name})

# 二维码页面
def qr_page(request, event_id):
    host = request.get_host()
    baseurl = "http://"+host+"/sign_index/"+str(event_id)+"/"
    # + url +"/sign_index/" + event_id  + "/"
    return render(request, "qrcode.html", {'baseurl': baseurl, 'event_id': event_id})


# 退出系统
@login_required
def logout(request):
    auth.logout(request) #退出登录
    response = HttpResponseRedirect('/index/')
    return response
