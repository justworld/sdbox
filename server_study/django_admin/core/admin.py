# coding: utf-8
from django.contrib import admin


class BaseModelAdmin(admin.ModelAdmin):
    # 分页显示，一页的数量
    list_per_page = 10

    # def get_action_choices(self, request, default_choices=admin.options.BLANK_CHOICE_DASH):
    #     """
    #     Return a list of choices for use in a form object.  Each choice is a
    #     tuple (name, description).
    #     """
    #     choices = [] + default_choices
    #     for func, name, description in self.get_actions(request).values():
    #         choice = (name, description % admin.options.model_format_dict(self.opts))
    #         choices.append(choice)
    #     return choices
