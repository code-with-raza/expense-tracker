from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ExpenseForm, IncomeForm
from django.db.models import Sum
from .models import Income, Expense
from django.shortcuts import get_object_or_404

# 1. Registration View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})

# 2. Corrected Home View (With @login_required decorator and single definition)
@login_required
def home_view(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    # NEW PRODUCTION ARCHITECTURE: Group expenses by category safely in database
    category_data = expenses.values('category').annotate(total=Sum('amount'))
    
    # Prepare clean lists for Chart.js
    
    # Production fallback optimization: Converts DB keys or human-readable names into cleanly formatted titles
    chart_labels = [item['category'].replace('_', ' ').replace('/', ' / ').title() for item in category_data]
    chart_values = [float(item['total']) for item in category_data]

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
    }
    return render(request, 'home.html', context)
# 3. Add Income View
@login_required
def add_income_view(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('home')
    else:
        form = IncomeForm()
    return render(request, 'add_transaction.html', {'form': form, 'title': 'Add Income'})

# 4. Add Expense View
@login_required
def add_expense_view(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('home')
    else:
        form = ExpenseForm()
    return render(request, 'add_transaction.html', {'form': form, 'title': 'Add Expense'})
@login_required
def edit_income_view(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'add_transaction.html', {'form': form, 'title': 'Edit Income'})

# 6. Edit Expense View
@login_required
def edit_expense_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'add_transaction.html', {'form': form, 'title': 'Edit Expense'})
# 7. Delete Income View
@login_required
def delete_income_view(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST' or request.method == 'GET':  # Kept simple via direct link click
        income.delete()
    return redirect('home')

# 8. Delete Expense View
@login_required
def delete_expense_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST' or request.method == 'GET':
        expense.delete()
    return redirect('home')