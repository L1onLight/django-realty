from django.contrib import admin
from .models import Item, Image, Review, Message, Favorite


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'created', 'updated', 'published', 'signed')
    list_display_links = ('id', 'title')
    list_filter = ("published", 'signed')
    search_fields = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}


class ImageAdmin(admin.ModelAdmin):
    search_fields = ("img",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", 'user', "rating")
    search_fields = ('user',)
    list_display_links = ('user',)


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', "user_email", 'product')
    search_fields = ('user', 'product', "user_email")
    list_display_links = ('user', "user_email", 'product')


# Register your models here.ad
admin.site.register(Item, ItemAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Favorite)
