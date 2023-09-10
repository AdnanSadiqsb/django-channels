from django.contrib import admin

from .models import Category, Channel, Server

# Register your models here.
admin.site.register(Category)
admin.site.register(Server)
admin.site.register(Channel)
admin.site.site_header = "Channel Management"
admin.site.site_title = "Channel Management"
