from django.db import models


class LanguageCodes(models.TextChoices):
    POLISH = ("pl",)
    GERMAN = ("de",)


class Language(models.Model):
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.code


class TranslationKey(models.Model):
    key = models.CharField(max_length=100)

    def __str__(self):
        return self.key


class Translation(models.Model):
    translation_key = models.ForeignKey(
        TranslationKey, on_delete=models.CASCADE, related_name="translations"
    )
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="translations"
    )
    value = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.translation_key} ({self.language}): {self.value}"

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["id", "language"], name="unique_translation"
    #         )
    #     ]
