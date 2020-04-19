import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Budget, Expense, Category
from .forms import BudgetForm, ExpenseForm


def budget_list(request):
    budget_list = Budget.objects.all()

    template = 'budget/list.html'
    context = {'budget_list': budget_list}

    return render(request, template, context)


def budget_detail(request, budget_slug):

    instance = get_object_or_404(Budget, slug=budget_slug)

    if request.method == 'GET':
        expense_list = instance.expenses.all()
        categories = Category.objects.filter(budget=instance)

        template = 'budget/detail.html'
        context = {
            'instance': instance,
            'expense_list': expense_list,
            'categories': categories,
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            amount = form.cleaned_data['amount']
            category_name = form.cleaned_data['category']

            category = get_object_or_404(
                Category, budget=instance, name=category_name)

            Expense.objects.create(
                budget=instance, title=title, amount=amount, category=category).save()

    elif request.method == 'DELETE':
        id = json.loads(request.body)['id']
        expense = get_object_or_404(Expense, id=id)
        expense.delete()
        return HttpResponse('')

    return redirect(instance.get_absolute_url())


def budget_add(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            categories = request.POST['categoriesString'].split(',')
            for category in categories:
                Category.objects.create(
                    budget=Budget.objects.get(id=instance.id),
                    name=category
                ).save()

            return redirect(instance.get_absolute_url())

    else:
        form = BudgetForm()

    template = 'budget/add.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
