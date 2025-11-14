# car_prediction/forms.py
from django import forms


class CarPredictionForm(forms.Form):
    GENDER_CHOICES = [
        (0, 'Female'),
        (1, 'Male'),
    ]

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
    )
    annual_salary = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Annual Salary', 'step': '1000'})
    )
    credit_card_debt = forms.FloatField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Credit Card Debt', 'step': '100'})
    )
    net_worth = forms.FloatField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Net Worth', 'step': '1000'})
    )