from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='incomes'),
    path('add-income/', views.addIncome, name='add-income'),
    path('search-income/', csrf_exempt(views.searchIncome), name='search-income'),
    path('edit-income/<int:id>', views.editIncome, name='edit-income'),
    path('delete-income/<int:id>', views.deleteIncome, name='delete-income'),
    path('income-summary/', views.income_summary, name='income-summary'),
    path('summary/', views.summary, name='in-summary'),


]