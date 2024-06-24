from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .models import Category, Expense
# Create your views here.

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def index(request):
    categories = Category.objects.all()
    return render(request, 'expenses/index.html')

@login_required(login_url='/authentication/login')
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'expenses/add_expense.html', context)