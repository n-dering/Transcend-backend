from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from django.db import transaction

from transcend import serializer
from transcend.serializer import TranslationSerializer
from .models import Translation, LanguageCodes

from rest_framework.request import Request
from django.db.models import QuerySet


class TranslationsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    lookup_field = "key"

    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()

        language_codes = queryset.values_list("language__code", flat=True).distinct()

        output = {}

        for code in language_codes:
            filtered_values = queryset.filter(language__code=code)
            serializer = self.get_serializer(filtered_values, many=True)
            output[code] = serializer.data

        return Response(output, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs) -> Response:
        queryset: QuerySet = self.get_queryset()
        key_value = request.data["key"]
        print(key_value)
        if key_value is None:
            return Response(
                {"error": "Key is required."}, status=status.HTTP_400_BAD_REQUEST
            )
        translation_data = request.data.copy()

        existing_rows = queryset.filter(key=key_value)
        if existing_rows.exists():
            return Response(
                {"error": "Key already exists."}, status=status.HTTP_400_BAD_REQUEST
            )

        display_data = {}

        with transaction.atomic():
            for langcode in LanguageCodes:
                translation_data["language.code"] = langcode

                serializer = self.get_serializer(data=translation_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                display_data[langcode.value] = serializer.validated_data
        return Response(display_data, status=status.HTTP_201_CREATED)

    def update(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        queryset: QuerySet = self.get_queryset()
        key_value = kwargs.get("key")

        existing_rows = queryset.filter(key=key_value)

        if not existing_rows.exists():
            return Response(
                {"error": "Key does not exist."}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(existing_rows.first(), data=data, partial=True)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
