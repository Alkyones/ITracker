from djongo import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from bson import ObjectId

class ExpensesManager(models.Manager):
    def get_by_id(self, id):
        try:
            return self.get(_id=ObjectId(id))
        except (self.model.DoesNotExist, ValueError):
            return None
        
        
class ExpensesModel(models.Model):
    _id = models.ObjectIdField()
    amount = models.FloatField()
    description = models.TextField()
    category = models.CharField(max_length=255)

    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(default=now)
    objects = ExpensesManager()
    def __str__(self):
        return f"{self.user} - {self.category}"

    @property
    def id(self):
        return str(self._id)
    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Expenses' 

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'
        

    def __str__(self):
        return self.name
