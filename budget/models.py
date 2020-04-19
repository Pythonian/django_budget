from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Budget(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.IntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Budget, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detail', kwargs={'budget_slug': self.slug})

    def budget_left(self):
        expense_list = Expense.objects.filter(budget=self)
        total_expense_amount = 0
        for expense in expense_list:
            total_expense_amount += expense.amount
        return self.budget - total_expense_amount

    def total_transactions(self):
        expense_list = Expense.objects.filter(budget=self)
        return len(expense_list)


class Category(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Expense(models.Model):
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-amount']
