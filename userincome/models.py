from djongo import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from bson import ObjectId

class IncomeManager(models.Manager):
    def get_by_id(self, id):
        try:
            return self.get(_id=ObjectId(id))
        except (self.model.DoesNotExist, ValueError):
            return None
class IncomeModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.FloatField()
    description = models.TextField()
    source_income = models.CharField(max_length=255)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(default=now)

    objects = IncomeManager()
    def __str__(self):
        return f"{self.user} - {self.source_income}"

    @property
    def id(self):
        return str(self._id)
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Incomes' 

class Source(models.Model):
    source_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.source_name
