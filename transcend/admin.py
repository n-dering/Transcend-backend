from django.contrib import admin
from .models import Language, Translation, TranslationKey


@admin.register(Language)
class Languages(admin.ModelAdmin):
    pass


@admin.register(Translation)
class Translations(admin.ModelAdmin):
    pass


@admin.register(TranslationKey)
class Translations(admin.ModelAdmin):
    pass
