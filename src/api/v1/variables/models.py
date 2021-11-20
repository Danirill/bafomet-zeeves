import uuid as uuid
from django.core.validators import FileExtensionValidator
from django.db import models


class Variable(models.Model):
    class Types(models.TextChoices):
        STRING = 'STRING'
        URL = 'URL'
        INT = 'INT'
        FLOAT = 'FLOAT'

    key = models.CharField(max_length=100, unique=True, null=False, blank=False)
    value = models.CharField(max_length=5000, null=False, blank=False)
    type = models.CharField(
        choices=Types.choices,
        default=Types.STRING,
        max_length=100,
        null=False,
        blank=False
    )

    @staticmethod
    def get_value(key):
        lambdas = {
            Variable.Types.STRING: lambda x: str(x),
            Variable.Types.URL: lambda x: str(x),
            Variable.Types.INT: lambda x: int(x),
            Variable.Types.FLOAT: lambda x: float(x),
        }
        try:
            var = Variable.objects.get(key=key)
            return lambdas[var.type](var.value)
        except Variable.DoesNotExist:
            return None

    def __str__(self):
        return f'{self.key} : {self.value}'
