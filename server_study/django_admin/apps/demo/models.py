# coding: utf-8
from django.db import models


class Demo(models.Model):
    name = models.CharField('demo名', max_length=20)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = "demo"
        verbose_name_plural = "demo管理"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField('部门名', max_length=128, help_text='一个部门的名字应该唯一', unique=True, db_index=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = "部门"
        verbose_name_plural = "部门管理"

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('职务', max_length=128, null=True, blank=True)

    class Meta:
        verbose_name = '职务'
        verbose_name_plural = '职务管理'

    # def get_absolute_url(self):
    #     return reverse('title-detail-view', args=(self.name,))

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(verbose_name='图片')
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, blank=False, null=True, )

    class Meta:
        verbose_name = '图片'
        verbose_name_plural = '图片管理'

    def __str__(self):
        return self.image.path


class Employe(models.Model):
    gender_choices = (
        (0, '未知'),
        (1, '男'),
        (2, '女'),
    )

    name = models.CharField('名称', max_length=128, help_text='员工的名字', null=False, blank=False, db_index=True)
    gender = models.IntegerField(choices=gender_choices, verbose_name='性别', default=0)
    idCard = models.CharField(max_length=18, verbose_name='身份证号', help_text='18位的身份证号码', blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name='手机号')
    birthday = models.DateField(verbose_name='生日')
    time = models.TimeField(verbose_name='时间', auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='部门',
                                   db_index=True)
    title = models.ForeignKey(Title, on_delete=models.SET_NULL, blank=False, null=True, verbose_name='职务',
                              db_index=True)

    enable = models.BooleanField(verbose_name='状态', default=True)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        verbose_name = "员工"
        verbose_name_plural = "员工管理"

    def __str__(self):
        return self.name


class Record(models.Model):
    type_choices = (
        (0, '收入'),
        (1, '支出'),
    )

    name = models.CharField(verbose_name='收支项', max_length=128, help_text='每一笔款项描述')
    money = models.DecimalField(verbose_name='金额', decimal_places=2, max_digits=9)
    create_date = models.DateTimeField(verbose_name='时间', auto_now=True)
    type = models.IntegerField(verbose_name='类型', choices=type_choices)

    class Meta:
        verbose_name = "收支"
        verbose_name_plural = "收支记录"

    def __str__(self):
        return self.name
