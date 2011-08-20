from polls.models import Poll, Vote
from django.contrib import admin

class VoteInline(admin.TabularInline):
    model = Vote
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["subject", "author", "description"]}),
        ("Date Information", {"fields": ["created", "expires"]})
    ]
    inlines = [VoteInline]

admin.site.register(Poll, PollAdmin)
