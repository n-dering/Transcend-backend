from rest_framework import serializers

from transcend.models import Language, Translation


class TranslationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translation
        fields = ["translation_key", "value", "updated_at"]


class LanguageTranslationSerializer(serializers.ModelSerializer):
    translations = TranslationSerializer(many=True, source="translations")

    class Meta:
        model = Language
        fields = ["code", "translations"]
