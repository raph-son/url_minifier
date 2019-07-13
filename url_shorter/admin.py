from django.contrib import admin
from url_shorter.models import Url

class UrlAdmin(admin.ModelAdmin):
    list_display = ('url','hash')

admin.site.register(Url, UrlAdmin)
