from django.contrib import admin
from .models import Language, Translation

@admin.register(Translation)
class Translations(admin.ModelAdmin):
    pass


@admin.register(Language)
class Languages(admin.ModelAdmin):
    pass