from django import forms

# 添加活动
class AddEventForm(forms.Form):
    name = forms.CharField(max_length=100)            # 签到会标题
    address = forms.CharField(max_length=200)         # 地址
    detail = forms.CharField(max_length=200)          # 描述

# 人员签到
class PeopleSingForm(forms.Form):
    realname = forms.CharField(max_length=50)
    empno = forms.CharField(max_length=50)
    user_agent = forms.CharField(max_length=200)
