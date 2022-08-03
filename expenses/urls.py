from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('search-expense/', csrf_exempt(views.search_expense), name='search-expense'),
    path('add-expense/', views.addExpense, name='add-expense'),
    path('edit-expense/<int:id>', views.editExpense, name='edit-expense'),
    path('delete-expense/<int:id>', views.deleteExpense, name='delete-expense'),
    path('expense-summary/',views.expense_summary, name='expense-summary'),
    path('summary/',views.summary, name='summary'),

]