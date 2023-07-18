from django.contrib import admin
from users.models import CustomUser


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name', 'phone', 'agent')
    list_display_links = ('id', 'email')
    list_filter = ("agent",)
    search_fields = ('id', 'email', 'phone', 'first_name', 'last_name')


admin.site.register(CustomUser, UserAdmin)
