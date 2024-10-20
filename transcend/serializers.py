from rest_framework import serializers

from transcend.models import Language, Translation


class TranslationSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source="translation_key.key")

    class Meta:
        model = Translation
        fields = ["key", "value", "updated_at"]


class LanguageTranslationSerializer(serializers.ModelSerializer):
    translations = TranslationSerializer(many=True, source="translations")

    class Meta:
        model = Language
        fields = ["code", "translations"]
