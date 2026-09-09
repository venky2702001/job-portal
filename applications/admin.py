from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'candidate', 'status', 'applied_at')
    search_fields = ('job__title', 'candidate__username')
    list_filter = ('status', 'applied_at')