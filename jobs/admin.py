from django.contrib import admin
from .models import Job
from applications.models import Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'salary', 'recruiter', 'created_at')
    search_fields = ('title', 'company', 'location')
    list_filter = ('location', 'company')


