from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Category, Expense
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)

    context = {
        'expenses': expenses,
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
    
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')
        