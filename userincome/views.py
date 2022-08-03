from django.shortcuts import render,redirect
from .models import IncomeModel, Source
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
import datetime


@login_required(login_url='/authentication/login')
def index(request):
    incomes = IncomeModel.objects.filter(user=request.user)
    pref_currency = UserPreferences.objects.filter(user=request.user)
    print(pref_currency)
    if pref_currency:
        pref_currency = UserPreferences.objects.get(user=request.user).currency.split('-')[0].strip()
    else:
        pref_currency = 'USD'

    paginated_incomes = Paginator(incomes, 5)
    page_total_number = request.GET.get('page')
    page_objs = Paginator.get_page(paginated_incomes, page_total_number)
    context = {
        'incomes':incomes,
        'page_objs':page_objs,
        'currency':pref_currency}
    
    return render(request, 'incomes/index.html',context)


def addIncome(request):
    sources = Source.objects.all()
    todayDate = datetime.datetime.today()
    context = {
        'sources': sources,
        'values': request.POST,
        'today_date': todayDate}

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST.get('description')
        source = request.POST.get('source')
        date = request.POST.get('income-date')
        if not amount:
            messages.error(request, 'Amount is required')
        if not description:
            messages.error(request, 'Description is required')
        if not source:
            messages.error(request, 'source is required')
        
        messages.success(request, 'Income added successfully')
        IncomeModel.objects.create(
            user=request.user,
            amount=amount,
            source_income=source,
            description=description,
            date =date)
        return redirect('incomes')
    
    return render(request, 'incomes/addIncome.html',context)


def editIncome(request, id):
    sources = Source.objects.all()
    income = IncomeModel.objects.get(pk=id)
    context = {
        'income': income,
        "Exvalues":income,
        "sources":sources
        }
    if request.method == 'GET':
        return render (request, 'incomes/editIncome.html', context)
    else:
        amount = request.POST.get('amount')
        description = request.POST.get('description')
        source = request.POST.get('source')
        date = request.POST.get('income-date')

        prm_list = [amount, source, date,description]
        if not any(prm_list):
            messages.info(request, 'Invalid input while editing income')
        else:
            income.user = request.user
            income.amount = amount
            income.category = source
            income.date = date
            income.description = description
            income.save()
            messages.success(request, 'Successfully edited income')
            return redirect('incomes')

        return render(request, 'incomes/editIncome.html', context)

def deleteIncome(request, id):
    income = IncomeModel.objects.get(id=id)
    income.delete()
    messages.success(request, 'Successfully deleted income')
    return redirect("incomes")
    
def searchIncome(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('search_text')

        incomes = IncomeModel.objects.filter(
            amount__istartswith=search_str, user = request.user)| IncomeModel.objects.filter(
                date__istartswith=search_str, user = request.user)| IncomeModel.objects.filter(
                    description__icontains=search_str, user = request.user)| IncomeModel.objects.filter(source_income__icontains=search_str, user = request.user)

        result = incomes.values()
        return JsonResponse(list(result),safe=False)


def income_summary(request):
    json_sending_data = {}
    today_date = datetime.date.today()
    month_ago = today_date-datetime.timedelta(days=30)
    incomes = IncomeModel.objects.filter(user=request.user, date__range=[month_ago,today_date])
    def get_source(income):
        return income.source_income

    source_list = list(set(map(get_source,incomes)))

    def get_category_amount(source):
        amount = 0
        filtered_incomes = incomes.filter(source_income=source)

        for income in filtered_incomes:
            amount += income.amount
        
        return amount
    
    for income in incomes:
        for source in source_list:
            json_sending_data[source] = get_category_amount(source)

    return JsonResponse({'income_source_data': json_sending_data}, safe=False  )

def summary(request):
    return render(request, 'incomes/summary.html')