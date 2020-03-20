from django.db import models


class Event(models.Model):
    """
    活动表
    """
    name = models.CharField(max_length=100)            # 活动标题
    address = models.CharField(max_length=200)         # 地址
    detail = models.CharField(max_length=200)          # 详细信息
    num = models.IntegerField(default=0)               # 已签到人数
    status = models.BooleanField(default=False)        # 状态默认为false,false状态不允许签到
    start_time = models.CharField(max_length=50)       # 签到开始时间,sting类型
    end_time = models.CharField(max_length=50)         # 签到结束时间,sting类型
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.name

class People(models.Model):
    """
    签到表
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联活动id
    realname = models.CharField(max_length=64)  # 姓名
    empno = models.CharField(max_length=20)     # 工号
    # email = models.EmailField()                 # 邮箱
    sign_time = models.DateTimeField(auto_now_add=True)  # 签到时间（自动获取当前时间）
    user_agent = models.CharField(max_length=200)    # 用户唯一标识码

    # class Meta:
    #     unique_together = ('empno', 'event')
    #     ordering = ['-id']

    def __str__(self):
        return self.realname
