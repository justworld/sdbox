from django.contrib import admin
from apps.demo.models import Demo


@admin.register(Demo)
class DemoAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_time')
    search_fields = ('name',)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
