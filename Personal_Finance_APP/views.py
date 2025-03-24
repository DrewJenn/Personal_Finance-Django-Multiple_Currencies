from django.shortcuts import render, redirect
from .authentication import CustomAuthBackend
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from moneyed import Money
import pandas as pd
from django.db import transaction
from .forms import SignUpForm, CustomLoginForm, CreateBankAccount, Deposit, Withdrawal, CloseAccount
from .models import BankAccount, BankRecord
from .helper_functions import views_help_functions as helper
from django.contrib.auth import login as auth_login

def index(request):
    return render(request, 'initial_views/home_page.html')


def login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']  
            password = form.cleaned_data['password']  
            custom_backend = CustomAuthBackend()
            user = custom_backend.authenticate(request=request, username=username, password=password)
            if user is not None:
                auth_login(request, user, backend='Personal_Finance_APP.authentication.CustomAuthBackend')
                messages.success(request, "You have been successfully logged in!")
                return redirect('user_home_screen')  
            else:
                messages.error(request, "Invalid username or password.")  
        else:
            messages.error(request, "Please fill out the form correctly") 
    else:
        form = CustomLoginForm() 
    return render(request, 'initial_views/login_page.html', {'form': form})



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()  # Now save user after setting password
            auth_login(request, user)  # Log the user in
            messages.success(request, "Your account has been created successfully!")
            return redirect('user_home_screen')  
        else:
            messages.error(request, "There was an error with your submission. Please try again.")
    else:
        form = SignUpForm()  
    return render(request, 'initial_views/signup_page.html', {'form': form})

@login_required
def home(request):
    user=request.user
    if user.bank_accounts.exists():   
        accounts = user.bank_accounts.all()
        total_named_balances = user.bank_accounts.values('account_holder_name', 'account_balance_currency').annotate(total_named_balance=Sum('account_balance'))
        total_balance = total_named_balances.values('account_balance_currency').annotate(total_named_balance=Sum('account_balance'))
        total_balance, conversion_currency = helper.home_get_total_balance(pd.DataFrame(total_balance))
        for entry in total_named_balances:
            currency = entry['account_balance_currency']
            balance = entry['total_named_balance']
            money_obj = Money(balance, currency)
            entry['total_named_balance'] = money_obj
    else:
        accounts, total_named_balances, total_balance, conversion_currency = None, None, 0.00, None
    return render(request, 'logged_in_views/user_home_screen.html', {'accounts':accounts,
            'total_named_balances':total_named_balances, 'total_balance':total_balance, 'conversion_currency':conversion_currency})



@login_required
def create_account(request):
    if request.method == 'POST':
        form = CreateBankAccount(request.POST)
        if form.is_valid():
            bank_account = form.save(commit=False)
            bank_account.user = request.user  
            bank_account.activate_account()
            return redirect('user_home_screen')  
    else:
        form = CreateBankAccount()
    return render(request, 'logged_in_views/create_account.html', {'form':form})



@login_required
def account_selection_deposit(request):
    form = Deposit(request.POST)
    user = request.user
    if user.bank_accounts.exists():
        accounts = user.bank_accounts.all()
    else:
        return redirect('user_home_screen')  
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        account = helper.get_selected_account(user, account_id)
        if form.is_valid():
            uninitialized_amount = form.cleaned_data['uninitialized_amount']
            deposit = form.save(commit=False)
            deposit.account_id = account  
            deposit.user = request.user  
            if account.process_deposit(uninitialized_amount):  
                deposit.new_balance = account.account_balance.amount
                deposit.deposit_record = True
                deposit.save() 
                return redirect('user_home_screen') 
            else:
                form.add_error(None, "Failed to process the deposit.")  
        else:
            form.add_error(None, "There was an error with the form.")  
    return render(request, 'logged_in_views/account_selection_deposit.html', {
        'accounts': accounts,
        'form': form,
    })


@login_required
def account_selection_withdrawal(request):
    form = Withdrawal(request.POST)
    user = request.user
    if user.bank_accounts.exists():
        accounts = user.bank_accounts.all()
    else:
        return redirect('user_home_screen')  
    if request.method == 'POST':
        account_id = request.POST.get('account_id')
        account = helper.get_selected_account(user, account_id)
        if form.is_valid():
            transaction_amount = form.cleaned_data['uninitialized_amount']
            withdrew = form.save(commit=False)
            withdrew.account_id = account  
            withdrew.user = request.user  
            if account.process_withdrawal(transaction_amount):  
                withdrew.new_balance = account.account_balance.amount
                withdrew.withdrawal_record = True
                withdrew.save() 
                return redirect('user_home_screen') 
            else:
                form.add_error(None, "Failed to process the withdrawal.")  
        else:
            form.add_error(None, "There was an error with the form.")  
    return render(request, 'logged_in_views/account_selection_withdrawal.html', {
        'accounts': accounts,
        'form': form
    })


@login_required
def transfer_money(request):
    user = request.user
    form_deposit = Deposit(request.POST or None)
    form_withdrawal = Withdrawal(request.POST or None)
    if user.bank_accounts.exists():
        accounts = user.bank_accounts.all()
    else:
        return redirect('user_home_screen')
    if request.method == 'POST':
        withdrawal_account_id, deposit_account_id = request.POST.get('withdrawal_account_id'), request.POST.get('deposit_account_id')
        withdrawal_amount = float(request.POST.get('uninitialized_amount'))
        deposit_amount = withdrawal_amount  
        withdrawal_account = helper.get_selected_account(user, withdrawal_account_id)
        deposit_account = helper.get_selected_account(user, deposit_account_id)
        if withdrawal_account.get_currency() != deposit_account.get_currency():
            exchange_rate = helper.get_exchange_rate(withdrawal_account.get_currency(), deposit_account.get_currency())
            deposit_amount = (deposit_amount * exchange_rate)
        if withdrawal_account.process_withdrawal(withdrawal_amount):
            with transaction.atomic():
                BankRecord.objects.create(  
                    account_id = withdrawal_account,
                    withdrawal_record = True,
                    new_balance = withdrawal_account.get_amount(),
                    uninitialized_amount = withdrawal_amount,
                )
                if deposit_account.process_deposit(deposit_amount):
                    BankRecord.objects.create( 
                        account_id = deposit_account,
                        deposit_record = True,
                        new_balance = deposit_account.get_amount(),
                        uninitialized_amount = deposit_amount,
                 )
            return redirect('user_home_screen')
        else:
            messages.error(request, 'Transaction failed. Please check the account balances and try again.')
            return render(request, 'logged_in_views/transfer_money.html', {'accounts':accounts, 'form_deposit':form_deposit, 'form_withdrawal':form_withdrawal})
    return render(request, 'logged_in_views/transfer_money.html', {'accounts':accounts, 'form_deposit':form_deposit, 'form_withdrawal':form_withdrawal})

@login_required
def close_account(request):
    user = request.user
    form = CloseAccount(request.POST)
    if user.bank_accounts.exists():
        accounts = user.bank_accounts.all()
    else:
        return redirect('user_home_screen')
    if request.method == 'POST':
        delete_id = request.POST.get('account_id')
        if form.is_valid():
            if delete_id:
               delete_account = BankAccount.objects.get(id=delete_id)
               delete_account.delete()
               return redirect('user_home_screen')
        else:
            form.add_error(None, 'Account failed to delete.')
    return render(request, 'logged_in_views/close_account.html', {'accounts': accounts, 'form':form})
