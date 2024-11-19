from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Translation, TranslationKey, Language
from .serializers import TranslationSerializer
from django.db import transaction
from rest_framework.views import APIView

from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class TranslationViewSet(APIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        languages = Language.objects.prefetch_related("translations").all()
        response_data = {}
        for language in languages:
            translations = language.translations.all()
            response_data[language.code] = TranslationSerializer(
                translations, many=True
            ).data
        return Response(response_data)

    @transaction.atomic
    @action(detail=False, methods=["post"])
    def create_or_update(self, request):
        data = request.data

        for language_code, translations in data.items():
            try:
                language = Language.objects.get(code=language_code)
            except Language.DoesNotExist:
                return Response(
                    {"error": f"Language with code '{language_code}' not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            for translation_data in translations:
                key_value = translation_data.get("translation_key")
                value = translation_data.get("value")

                if not key_value or not value:
                    return Response(
                        {"error": "Both 'translation_key' and 'value' are required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Get or create the translation key
                translation_key, _ = TranslationKey.objects.get_or_create(key=key_value)

                # Get or create the translation entry
                translation, created = Translation.objects.update_or_create(
                    translation_key=translation_key,
                    language=language,
                    defaults={"value": value},
                )

        return Response(
            {"message": "Translations created/updated successfully."},
            status=status.HTTP_200_OK,
        )
