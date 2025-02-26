from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BankAccount, BankRecord
import pandas as pd
from moneyed import Money
from .helper_functions import chart_views_help_functions as helper
import matplotlib
matplotlib.use('Agg')

def account_details(request, id):
    account = get_object_or_404(BankAccount, id=id)
    currency = account.get_currency()
    records = BankRecord.objects.filter(account_id=account).order_by('transaction_date')
    dates, balances = [account.initial_account_date], [float(account.get_initial_amount())]       
    transaction = [Money(account.get_initial_amount(), currency)]
    transaction_type = ["Deposit"]
    for record in records:    
        if record.transaction_date and record.new_balance:
            if record.withdrawal_record:
                transaction.append(Money(record.uninitialized_amount, currency))
                transaction_type.append("Withdrawal")
            else:
                transaction.append(record.transaction_amount)
                transaction_type.append("Deposit")
            dates.append(record.transaction_date)
            balances.append(float(record.new_balance))
    table_html = pd.DataFrame({'Date':dates, 'Amount':transaction, 'Balance':balances, 'Transaction Type':transaction_type})
    table_html_1 = []
    for i in range(table_html.shape[0]):
        table_html_1.append(Money(table_html.at[i, 'Balance'], currency))
    table_html["Balance"] = table_html_1
    table_html = table_html[table_html["Amount"] != Money(0.00, currency)]
    table_html = table_html.to_html(index=False)
    return render(request, 'data_display/account_details.html', {'table_html':table_html})



@login_required
def aggregate_values_display(request, account_holder_name, account_balance_currency):
    if account_holder_name == 'all':
        accounts = BankAccount.objects.filter(user=request.user)       
        answer = helper.aggregate_all(accounts, account_balance_currency)
        table_html = answer.to_html(index=False, col_space=90)
    else:
        accounts = BankAccount.objects.filter(account_holder_name=account_holder_name, user=request.user, account_balance_currency=account_balance_currency)   #only handles one currency
        answer = helper.aggregate_df_by_name(accounts, account_balance_currency)    
        table_html = answer.to_html(index=False, col_space=90)
    return render(request, 'data_display/aggregate_values_display.html', {'table_html':table_html})
