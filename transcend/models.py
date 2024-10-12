from django.db import models


class Language(models.Model):
        class LanguageCode(models.TextChoices):
            POLISH = 'PL',
            GERMAN = 'DE',


        name = models.CharField(max_length=100)
        code = models.CharField(max_length=10, choices=LanguageCode.choices)

        def  __str__(self):
            return self.name



class Translation(models.Model):
    key = models.CharField()
    value = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['key', 'language'], name='unique_translation')
        ]

    def __str__(self):
        return f"{self.key}_{self.language}"
