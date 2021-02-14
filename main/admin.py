from django.contrib import admin
from main import models


@admin.register(models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("name", "active")