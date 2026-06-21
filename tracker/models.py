from django.db import models
from django.contrib.auth.models import User

# 1. Corrected Income Model
class Income(models.Model):
    CATEGORY_CHOICES = [
        ('salary', 'Salary'),
        ('business', 'Business'),
        ('gift', 'Gift'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Changed max_length to max_digits
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, default='Bank Transfer')

    def __str__(self):
        return f"{self.title} - {self.amount}"


# 2. Corrected Expense Model
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('rent', 'Rent/Utilities'),
        ('entertainment', 'Entertainment'),
        ('transport', 'Transportation'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Changed max_length to max_digits
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    date = models.DateField()

    description = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, default='Cash')

    def __str__(self):
        return f"{self.title} - {self.amount}"