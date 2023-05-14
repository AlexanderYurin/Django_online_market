from django.contrib import admin
from app_users.models import Profile, Order


class ProfileAdmin(admin.ModelAdmin):
    list_filter = ('first_name',)
    list_display = ('id', 'first_name', 'last_name', 'balance')


class OrderAdmin(admin.ModelAdmin):
    list_filter = ('profile', 'created_at')
    list_display = ('profile', 'good', 'created_at', 'quantity')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Order, OrderAdmin)
