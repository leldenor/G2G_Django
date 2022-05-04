from django.contrib import admin

from app.models import Item, OrderItem, UserProfile


admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
