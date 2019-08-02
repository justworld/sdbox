# coding: utf-8
from django.db import models


class Demo(models.Model):
    name = models.CharField('用户id', max_length=20)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)


