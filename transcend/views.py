from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from django.db import transaction

from transcend import serializer
from transcend.serializer import TranslationSerializer
from .models import Translation, LanguageCodes
from rest_framework.decorators import action

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

    @action(methods=["patch"], detail=False)
    def updateFields(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        queryset: QuerySet = self.get_queryset()

        if not isinstance(data, list):
            data = [data]

        updated_items = []
        errors = []

        with transaction.atomic():
            for item in data:
                existing_rows = queryset.filter(pk=item.get("id"))
                if not existing_rows.exists():
                    errors.append(
                        {"id": item.get("id"), "error": "Key does not exist."}
                    )
                    continue

                serializer = self.get_serializer(
                    existing_rows.first(), data=item, partial=True
                )
                try:
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    updated_items.append(serializer.data)
                except Exception as e:
                    errors.append({"id": item.get("id"), "error": str(e)})

        if errors:
            return Response(
                {"updated": updated_items, "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(updated_items, status=status.HTTP_200_OK)
