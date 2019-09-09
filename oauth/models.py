from django.db import models

# Create your models here.
from admin.models import User

# 用户登录的类型
type = (
    ('1', 'github'),
    ('2', 'qq'),
    ('3', 'wechat')
)


class OAuth(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)  # User为本网站的用户模型，每个第三方账号都要绑定本站账号
    openid = models.CharField(max_length=100, default='')
    type = models.CharField(max_length=1, choices=type)
