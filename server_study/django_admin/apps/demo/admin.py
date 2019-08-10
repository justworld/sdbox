import datetime
from django.contrib import admin
from import_export import resources
from django.conf.urls import url
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

from core.admin import BaseModelAdmin
from .filters import AgeListFilter
from .models import Demo, Department, Image, Title, Employe, Record


@admin.register(Demo)
class DemoAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'create_time')

    search_fields = ('name',)

    actions_on_top = True

    # 增加自定义按钮
    actions = ['custom_dialog']

    def get_urls(self):
        urls = super(DemoAdmin, self).get_urls()
        my_urls = [
            url(r'^custom_dialog/$', self.admin_site.admin_view(self.custom_dialog), name='custom_dialog'),
        ]
        return my_urls + urls

    def custom_dialog(self, request):
        from django.http.response import JsonResponse
        return JsonResponse({'msg': 'sdf'})

    # 显示的文本，与django admin一致
    custom_dialog.short_description = '测试按钮'
    custom_dialog.url = '/admin/demo/demo/custom_dialog'


# Register your models here.
@admin.register(Department)
class DepartmentAdmin(BaseModelAdmin):
    # 要显示的字段
    list_display = ('id', 'name', 'create_time')

    # 需要搜索的字段
    search_fields = ('name',)

    actions_on_top = True


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Title)
class TitleAdmin(BaseModelAdmin):
    # 要显示的字段
    list_display = ('id', 'name')

    # 需要搜索的字段
    search_fields = ('name',)

    inlines = [
        ImageInline,
    ]


@admin.register(Employe)
class EmployeAdmin(BaseModelAdmin):
    list_display = ('id', 'name', 'gender', 'phone', 'birthday', 'department', 'enable', 'create_time')
    # search_fields = ('name', 'enable', 'idCard', 'department')
    search_fields = ('name', 'department__name')
    raw_id_fields = ('department', 'title')
    list_filter = ('department', AgeListFilter)
    # list_filter = (AgeListFilter, 'department', 'create_time', 'birthday', 'time', 'enable', 'gender')

    list_display_links = ('name',)

    list_editable = ('department', 'phone', 'birthday', 'enable', 'gender')

    date_hierarchy = 'create_time'
    # 增加自定义按钮
    actions = ['make_copy', 'custom_button']

    def custom_button(self, request, queryset):
        pass

    # 显示的文本，与django admin一致
    custom_button.short_description = '测试按钮'
    # icon，参考element-ui icon与https://fontawesome.com
    custom_button.icon = 'fas fa-audio-description'

    # 指定element-ui的按钮类型，参考https://element.eleme.cn/#/zh-CN/component/button
    custom_button.type = 'danger'

    # 给按钮追加自定义的颜色
    custom_button.style = 'color:black;'

    def make_copy(self, request, queryset):
        ids = request.POST.getlist('_selected_action')
        for id in ids:
            employe = Employe.objects.get(id=id)
            Employe.objects.create(
                name=employe.name,
                idCard=employe.idCard,
                phone=employe.phone,
                birthday=employe.birthday,
                department_id=employe.department_id
            )

    make_copy.short_description = '复制员工'


class ProxyResource(resources.ModelResource):
    class Meta:
        model = Record


@admin.register(Record)
class RecordAdmin(ImportExportActionModelAdmin):
    resource_class = ProxyResource

    list_display = ('id', 'name', 'type', 'money', 'create_date')
    list_per_page = 10
