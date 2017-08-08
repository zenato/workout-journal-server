from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Event, Post, Performance


class WorkoutAdminSite(AdminSite):
    site_header = 'Workout administration'


class PerformanceInline(admin.TabularInline):
    model = Performance
    extra = 1


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'value',)
    list_filter = ('name',)
    ordering = ['name', ]
    empty_value_display = '-'


class PostAdmin(admin.ModelAdmin):
    list_display = ('formatted_workout_date', 'remark',)
    list_filter = ['workout_date', ]
    ordering = ['-workout_date', ]
    inlines = [PerformanceInline]


admin.site = WorkoutAdminSite()
admin.site.register(Event, EventAdmin)
admin.site.register(Post, PostAdmin)
