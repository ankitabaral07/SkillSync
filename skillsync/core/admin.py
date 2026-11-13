from django.contrib import admin
from .models import Profile, Skill, Message, MessageRequest, Notification, Project


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'skills_to_teach', 'skills_to_learn')
    search_fields = ('user__username', 'skills_to_teach', 'skills_to_learn')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'skill_type', 'created_at')
    list_filter = ('skill_type',)
    search_fields = ('user__username', 'name')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'content')


@admin.register(MessageRequest)
class MessageRequestAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status', 'created_at')
    list_filter = ('status',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'sender', 'notification_type', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'required_skills', 'created_at')
    search_fields = ('title', 'owner__username')