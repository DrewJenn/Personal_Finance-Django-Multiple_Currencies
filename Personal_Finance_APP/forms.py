from django import forms
from .models import BankAccount, BankRecord, User
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate



class SignUpForm(forms.ModelForm):
    confirmPassword = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label="Verify Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'firstName', 'lastName', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Display Name'})
        }
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'firstName': 'First Name',
            'lastName': 'Last Name',
            'password': 'Password',
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Error: Username already taken")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')

        if password and confirmPassword and password != confirmPassword:
            self.add_error('confirmPassword', "Error: Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user
    




class CustomLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data





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
