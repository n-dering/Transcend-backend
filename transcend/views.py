from rest_framework.response import Response
from rest_framework import status, viewsets, mixins

from transcend.serializer import TranslationSerializer
from .models import Translation

from rest_framework.response import Response
from rest_framework.request import Request
from django.db.models import QuerySet


class TranslationsViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Translation.objects.all()
    serializer_class = TranslationSerializer
    lookup_field = "key"

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        # serializer = self.get_serializer(queryset, many=True)

        language_codes = queryset.values_list("language__code", flat=True).distinct()

        output = {}

        for code in language_codes:
            filtered_values = queryset.filter(language__code=code).values()
            output[code] = filtered_values  # Add the results to the output dictionary

        return Response(output, status=status.HTTP_200_OK)

    def create(self, request: Request, *args, **kwargs) -> Response:
        queryset: QuerySet = self.get_queryset()
        print("test")

        # Pobieramy dane z requestu
        key_value = request.data.get("key")
        language_code_key = request.data.get("language.code")

        # Filtrujemy queryset na podstawie klucza i kodu języka
        filtered_row: QuerySet = queryset.filter(
            key=key_value, language__code=language_code_key
        )
        # update or create new
        if filtered_row.exists():
            # Aktualizacja istniejącego rekordu
            instance = filtered_row.first()
            serializer = self.get_serializer(
                instance, data=request.data, partial=True
            )  # partial=True dla aktualizacji
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Zapis aktualizacji
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Tworzenie nowego rekordu
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # Zapis nowego rekordu
            return Response(serializer.data, status=status.HTTP_201_CREATED)
