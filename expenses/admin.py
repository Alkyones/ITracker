from django.contrib import admin
from .models import ExpensesModel,Category
# Register your models here.

admin.site.register(ExpensesModel)
admin.site.register(Category)
