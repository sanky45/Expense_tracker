from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Category, Expense
from django.utils import timezone

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        login(request, user)
        return redirect('dashboard')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    categories = Category.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'expenses': expenses, 'categories': categories})

@login_required
def add_expense(request):
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category_id = request.POST['category']
        date = request.POST['date']
        category = get_object_or_404(Category, id=category_id, user=request.user)
        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description,
            date=date
        )
        messages.success(request, 'Expense added successfully.')
        return redirect('dashboard')
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expense_form.html', {'categories': categories})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        category_id = request.POST['category']
        date = request.POST['date']
        category = get_object_or_404(Category, id=category_id, user=request.user)
        expense.amount = amount
        expense.description = description
        expense.category = category
        expense.date = date
        expense.save()
        messages.success(request, 'Expense updated successfully.')
        return redirect('dashboard')
    categories = Category.objects.filter(user=request.user)
    return render(request, 'expense_form.html', {'expense': expense, 'categories': categories})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully.')
    return redirect('dashboard')