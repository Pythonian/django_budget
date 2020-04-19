from django.contrib import admin
from .models import Budget, Expense, Category


admin.site.register(Budget)
admin.site.register(Expense)
admin.site.register(Category)
