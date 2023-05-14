from django.contrib import admin
from app_shops.models import Good, Category, Shop


class GoodAdmin(admin.ModelAdmin):
    list_filter = ('title', 'price', 'quantity', 'shop', 'bought')
    list_display = ('title', 'price', 'quantity', 'shop', 'bought')
    list_editable = ('price', 'quantity')


class CategoryAdmin(admin.ModelAdmin):
    list_filter = ('title',)
    list_display = ('title',)


class ShopAdmin(admin.ModelAdmin):
    list_filter = ('title',)
    list_display = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Good, GoodAdmin)
