from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import ExpensesModel,Category
from userpreferences.models import UserPreferences
from django.contrib.auth.models import User

import json
import datetime
from django.http import JsonResponse


def search_expense(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('search_text')

        expenses = ExpensesModel.objects.filter(
            amount__istartswith=search_str, user = request.user)| ExpensesModel.objects.filter(
                date__istartswith=search_str, user = request.user)| ExpensesModel.objects.filter(
                    description__icontains=search_str, user = request.user)| ExpensesModel.objects.filter(category__icontains=search_str, user = request.user)

        result = expenses.values()
        return JsonResponse(list(result),safe=False)



@login_required(login_url='/authentication/login')
def index(request):
    expenses = ExpensesModel.objects.filter(user=request.user)
    
    try:
        pref_currency = UserPreferences.objects.get(user=request.user).currency
    except:
        pref_currency = 'USD - Dollar'
    paginated_expenses = Paginator(expenses, 5)
    page_total_number = request.GET.get('page')
    page_objs = Paginator.get_page(paginated_expenses, page_total_number)
    context = {
        'expenses':expenses,
        'page_objs':page_objs,
        'currency':pref_currency}
    
    return render(request, 'expenses/index.html',context)


def addExpense(request):
    categories = Category.objects.all()
    todayDate = datetime.datetime.now()
    context = {
        'categories': categories,
        'today_date':todayDate,
        'values': request.POST}

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('expense-date')
        if not amount:
            messages.error(request, 'Amount is required')
        if not description:
            messages.error(request, 'Description is required')
        if not category:
            messages.error(request, 'Category is required')
        
        messages.success(request, 'Expense added successfully')
        ExpensesModel.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            description=description,
            date =date)
        return redirect('expenses')
    
    return render(request, 'expenses/addExpense.html',context)


def editExpense(request, id):
    categories = Category.objects.all()
    expense = ExpensesModel.objects.get(pk=id)
    context = {
        'expense':expense,
        "Exvalues":expense,
        "categories":categories
        }
    if request.method == 'GET':
        return render (request, 'expenses/editExpense.html', context)
    else:
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        category = request.POST.get('category')
        date = request.POST.get('expense-date')

        prm_list = [amount, category, date,description]
        if not any(prm_list):
            messages.success(request, 'Invalid input while editing expense')
        else:
            expense.user = request.user
            expense.amount = amount
            expense.category = category
            expense.date = date
            expense.description = description
            expense.save()
            messages.success(request, 'Successfully edited expense')
            return redirect('expenses')

        return render(request, 'expenses/editExpense.html', context)

def deleteExpense(request, id):
    expense = ExpensesModel.objects.get(id=id)
    expense.delete()
    messages.success(request, 'Successfully deleted expense')
    return redirect("expenses")


def expense_summary(request):
    json_sending_data = {}
    today_date = datetime.date.today()
    month_ago = today_date-datetime.timedelta(days=30)
    expenses = ExpensesModel.objects.filter(user=request.user, date__range=[month_ago,today_date])
    print(expenses)
    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category,expenses)))

    def get_category_amount(category):
        amount = 0
        filtered_expenses = expenses.filter(category=category)

        for expense in filtered_expenses:
            amount += expense.amount
        
        return amount
    
    for expense in expenses:
        for category in category_list:
            json_sending_data[category] = get_category_amount(category)

    return JsonResponse({'expense_category_data': json_sending_data}, safe=False  )

def summary(request):
    return render(request, 'expenses/summary.html')