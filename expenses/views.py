from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
import csv
import xlwt
# from django.contrib.auth.models import UserPreference
# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    user_preferences = UserPreference.objects.filter(user=request.user).first()
    # currency = UserPreference.objects.get(user=request.user).currency

    if not user_preferences:
        currency = "USD"
    else:
        currency = user_preferences.currency

    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        # import pdb
        # pdb.set_trace()

        # validate amount input
        amount = request.POST['amount']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        
        # validate description input
        description = request.POST['description']
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expense.html', context)
        
        # category selection
        category = request.POST['category']

        # date input
        date = request.POST['expense_date']

        # owner input should also be passed

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')
    
@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def expense_edit(request, id):
    categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'expense': expense,
        'values': expense,
        'categories' : categories
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        # validate amount input
        amount = request.POST['amount']
        # import pdb
        # pdb.set_trace()
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        
        # validate description input
        description = request.POST['description']
        
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)
        
        # category selection
        category = request.POST['category']

        # date input
        date = request.POST['expense_date']

        # owner input should also be passed

        # Expense.objects.create(owner=request.user, amount=amount, date=date,
        #                        category=category, description=description)
        expense.owner=request.user
        expense.amount=amount
        expense.date=date
        expense.category=category 
        expense.description=description
        expense.save()
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')
        
def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date-datetime.timedelta(days=30*6)

    expenses = Expense.objects.filter(owner=request.user, 
                                      date__gte=six_months_ago, date__lte = todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category
    
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount+=item.amount
        return amount
    
    category_list = list(set(map(get_category, expenses)))

    for x in expenses:
        for y in category_list:
            finalrep[y]=get_expense_category_amount(y)

    return JsonResponse({'expense_category_data':finalrep}, safe=False)

def stats_view(request):
    return render(request, 'expenses/stats.html')

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition']='attachment; filename=Expenses'+\
        str(datetime.datetime.now())+'.csv'
    
    writer = csv.writer(response)
    writer.writerow(['Data','Amount','Description','Category'])

    expenses = Expense.objects.filter(owner = request.user)
    for expense in expenses:
        writer.writerow([expense.date, expense.amount, 
                         expense.description, expense.category])
        
    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition']='attachment; filename=Expenses'+\
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8') # workbook
    ws = wb.add_sheet('Expenses') #worksheet
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True # font style only for headers

    columns = ['Data','Amount','Description','Category']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle() #resetting font style
    rows = Expense.objects.filter(owner=request.user).values_list('date','amount','description','category' ) # dynamic rows

    for row in rows:
        row_num+=1

        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style) 
            # conerting 3rd parameter to str to avoid possible rendering issues

    wb.save(response)

    return response

