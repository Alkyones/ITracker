from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class IncomeModel(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    source_income = models.CharField(max_length=255)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    date = models.DateField(default=now)

    def __str__(self):
        return f"{self.user} - {self.source_income}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Incomes' 

class Source(models.Model):
    source_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.source_name
