from django.contrib import admin

from task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['pk', 'owner', 'place', 'time', 'action', 'pleasant_task', 'related_task', 'periodicity', 'award',
                    'duration', 'is_public']
