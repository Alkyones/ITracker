from django.urls import  path
from . import views


urlpatterns = [
    path('', views.index, name='preferences'),
    path('add/', views.saveSourceExpense, name='save_income_expense'),
]