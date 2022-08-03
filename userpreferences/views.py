from pyexpat.errors import messages
from re import S
from django.conf import settings
from django.shortcuts import render,redirect
import os,json 
from django.contrib import messages

from expenses.models import Category
from userincome.models import Source
from .models import UserPreferences
# Create your views here.


def index(request):
    userPrefExists = UserPreferences.objects.filter(user=request.user).exists()
    userPref = None
    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as f:
        data = json.load(f)
        for k,v in data.items():
            currency_data.append({'name': k, 'value': v})

    if userPrefExists:
        userPref = UserPreferences.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'preferences/index.html', {'currencies': currency_data,'user_preferences': userPref})
    else:
        currency = request.POST.get('currency')
        if userPrefExists:
            userPref.currency = currency
            userPref.save()
        else:
            UserPreferences.objects.create(user=request.user, currency=currency)
        
        messages.success(request, "Currency has been saved successfully")
        return render(request, 'preferences/index.html', {'currencies': currency_data,'user_preferences': userPref})


def saveSourceExpense(request):
    if request.method == 'POST':
        type = request.POST.get('valueType')
        name = request.POST.get('valueName')
        if type and name:
            if type == 'income':
                if not Source.objects.filter(source_name=name).exists():
                    Source.objects.create(source_name=name)
                    messages.success(request, "Source has been saved successfully")
            if type == 'expense':
                if not Category.objects.filter(name=name).exists():
                    Category.objects.create(name=name)
                    messages.success(request, "Expense category has been saved successfully")
        return redirect("save_income_expense")
    else:
        return render(request, 'preferences/add_expense_source.html')
