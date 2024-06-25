from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
import json
from django.http import JsonResponse
import datetime

# Create your views here.

def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    
@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency

    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        # import pdb
        # pdb.set_trace()

        # validate amount input
        amount = request.POST['amount']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        
        # validate description input
        description = request.POST['description']
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)
        
        # category selection
        source = request.POST['source']

        # date input
        date = request.POST['income_date']

        # owner input should also be passed

        UserIncome.objects.create(owner=request.user, amount=amount, date=date,
                               source=source, description=description)
        
        messages.success(request, 'Record saved successfully')
        return redirect('income')
    

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def income_edit(request, id):
    sources = Source.objects.all()
    income = UserIncome.objects.get(pk=id)
    context = {
        'income': income,
        'values': income,
        'sources' : sources
    }

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        # validate amount input
        amount = request.POST['amount']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        
        # validate description input
        description = request.POST['description']
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)
        
        # source selection
        source = request.POST['source']

        # date input
        date = request.POST['income_date']

        # owner input should also be passed

        # Expense.objects.create(owner=request.user, amount=amount, date=date,
        #                        category=category, description=description)
        income.owner=request.user
        income.amount=amount
        income.date=date
        income.source=source 
        income.description=description
        income.save()
        messages.success(request, 'Record updated successfully')
        return redirect('income')
    
def delete_income(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record removed')
    return redirect('income')


def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)

    income = UserIncome.objects.filter(owner=request.user, 
                                      date__gte=six_months_ago, date__lte = todays_date)
    finalrep = {}

    def get_category(income):
        return income.source
    
    def get_income_source_amount(source):
        amount = 0
        filtered_by_category = income.filter(source=source)
        for item in filtered_by_category:
            amount+=item.amount
        return amount
    
    source_list = list(set(map(get_category, income)))

    for x in income:
        for y in source_list:
            finalrep[y]=get_income_source_amount(y)

    return JsonResponse({'income_source_data':finalrep}, safe=False)

def stats_view(request):
    return render(request, 'income/stats.html')    