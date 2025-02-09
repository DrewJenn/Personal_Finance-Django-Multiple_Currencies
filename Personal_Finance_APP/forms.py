from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import BankAccount, BankRecord



class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.',
        }
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm your password'}),
        }

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}))


class CreateBankAccount(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = [
            'account_holder_name',
            'bank_name',
            'account_type',
            'interest_rate',
            'compound_interest',
            'compound_interest_frequency',
            'interest_payout_frequency',
            'account_balance',
        ]
        labels = {
            'account_holder_name':'Name',
            'bank_name':'Bank Name',
            'account_type':'Account Type',
            'interest_rate':'Interest Rate',
            'compound_interest':'Compounding Interest',
            'compound_interest_frequency':'Compounding Interest Frequency',
            'interest_payout_frequency':'Interest Payout Frequency',
            'account_balance':'Account Balance'
        }

class Deposit(forms.ModelForm):
    class Meta:
        model = BankRecord
        fields = ['uninitialized_amount', 'account_id']


class Withdrawal(forms.ModelForm):
    class Meta:
        model = BankRecord
        fields = ['uninitialized_amount', 'account_id']
    
class CloseAccount(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_id']