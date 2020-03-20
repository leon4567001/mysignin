"""mysignin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hr_signin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index', views.hello), # 测试路径为127.0.0.1:8000/index
    path('', views.index), # 127.0.0.1:8000 默认打开首页
    path('index/', views.index), # 退出的时候用
    path('login_action/', views.login_action), # 登录表单提交后交给action处理
    path('event_manage/', views.event_manage), # 活动管理页面
    path('add_event/', views.add_event), # 添加活动页面
    path('search_name/', views.search_name), # 查找活动页面
    path('people_manage/<int:event_id>/', views.people_manage), #人员管理页面
    path('search_people/', views.search_people), #姓名查找页面
    path('swich_action/<int:event_id>/', views.swich_action), #开关页面
    path('sign_index/<int:event_id>/', views.sign_index), #签到页面
    path('qr_page/<int:event_id>/', views.qr_page), #二维码页面
    path('logout/', views.logout), # 退出页面
]
