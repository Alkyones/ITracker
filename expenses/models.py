from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class ExpensesModel(models.Model):
    amount = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=255)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    date = models.DateField(default=now)

    def __str__(self):
        return f"{self.user} - {self.category}"

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Expenses' 

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'
        

    def __str__(self):
        return self.name
