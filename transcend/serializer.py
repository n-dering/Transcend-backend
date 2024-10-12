from typing import Any, Dict
from rest_framework import serializers
from .models import Translation, Language
from django.db.models import QuerySet


class LanguageSerializer(serializers.ModelSerializer):
    name: serializers.CharField = serializers.CharField(
        read_only=True, write_only=False
    )

    class Meta:
        model: type = Language
        fields: list[str] = ["name", "code"]


class TranslationSerializer(serializers.ModelSerializer):
    language: LanguageSerializer = LanguageSerializer()

    class Meta:
        model: type = Translation
        fields: list[str] = ["key", "value", "language"]

    def create(self, validated_data):
        language_data = validated_data.pop("language")
        language, _ = Language.objects.get_or_create(**language_data)
        validated_data["language"] = language
        return super().create(validated_data)

    def update(self, instance, validated_data):
        language_data = validated_data.pop("language")
        language, _ = Language.objects.get_or_create(**language_data)
        validated_data["language"] = language
        return super().update(instance, validated_data)
