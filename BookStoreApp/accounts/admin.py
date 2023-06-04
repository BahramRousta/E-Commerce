from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    list_display = ('user', 'email', 'city', 'province')
    list_filter = ('city', 'province')
    search_fields = ('user',)
    ordering = ('user',)
    list_editable = ('city', 'province')


admin.site.register(Profile, ProfileAdmin)
