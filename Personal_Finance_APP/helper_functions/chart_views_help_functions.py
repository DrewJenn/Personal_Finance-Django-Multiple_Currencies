from Personal_Finance_APP.models import BankRecord
import pandas as pd
from moneyed import Money
import numpy as np
from .views_help_functions import get_exchange_rate  
import matplotlib
matplotlib.use('Agg')



def aggregate_all(accounts, currency):
    transaction, dates = [], []
    deposit, withdrawal = [], []
    diff_currency_accounts = {}
    for account in accounts:
        amount = float(account.get_initial_amount())
        if account.get_currency() != currency:
            exchange_rate = get_exchange_rate(account.get_currency(), currency)
            diff_currency_accounts[account] = exchange_rate
        else:
            exchange_rate = 1
        transaction.append(round(amount * exchange_rate, 2))      
        deposit.append(True)
        withdrawal.append(False)
        dates.append(account.initial_account_date)            
    account_ids = [account.id for account in accounts]      
    records = BankRecord.objects.filter(account_id__in=account_ids)   
    for record in records:
        bank_account = record.account_id
        if record.deposit_record:
            deposit.append(True)
            withdrawal.append(False)
        else:
            deposit.append(False)
            withdrawal.append(True)
        if bank_account in diff_currency_accounts:
            exchange_rate = diff_currency_accounts[bank_account]
        else:
            exchange_rate = 1
        amount = float(record.uninitialized_amount)
        transaction.append(round(amount * exchange_rate, 2))
        dates.append(record.transaction_date)
    table_html = pd.DataFrame({'Date':pd.to_datetime(dates), 'Amount':transaction, 'Deposit':deposit, 'Withdrawal':withdrawal})
    table_html = table_html.sort_values(by='Date', ascending=True).reset_index().drop(columns='index')
    table_html = aggregate_by_name_GETBALANCE(table_html, currency)
    return table_html


def aggregate_df_by_name(accounts, currency):
    transaction, dates = [], []
    deposit, withdrawal = [], []
    for account in accounts:
        transaction.append(round(float(account.get_initial_amount()), 2))      
        deposit.append(True)
        withdrawal.append(False)
        dates.append(account.initial_account_date)     
    account_ids = [account.id for account in accounts]        
    records = BankRecord.objects.filter(account_id__in=account_ids)    
    for record in records:
        if record.deposit_record:
            deposit.append(True)
            withdrawal.append(False)
        else:
            deposit.append(False)
            withdrawal.append(True)
        transaction.append(round(float(record.uninitialized_amount), 2))
        dates.append(record.transaction_date)
    table_html = pd.DataFrame({'Date':pd.to_datetime(dates), 'Amount':transaction, 'Deposit':deposit, 'Withdrawal':withdrawal})
    table_html = table_html.sort_values(by='Date', ascending=True).reset_index().drop(columns='index')
    table_html = aggregate_by_name_GETBALANCE(table_html, currency)
    return table_html




def aggregate_by_name_GETBALANCE(table_html, currency):
    table_html['Balance'], balance = np.nan, 0
    for i in range(table_html.shape[0]):
        if table_html.iat[i, 2]:
            balance += table_html.iat[i, 1]
            transaction_type = 'Deposit'
        else:
            balance -= table_html.iat[i, 1]
            transaction_type = 'Withdrawal'
        table_html.iat[i, 4] = balance
        table_html.iat[i, 2] = transaction_type
    table_html = table_html[['Date', 'Amount', 'Balance', 'Deposit']].rename(columns = {'Deposit':'Transaction Type'})
    table_html = convert_df_money_objects(table_html, currency)
    return table_html




def convert_df_money_objects(table_html, currency):
    try:
        for i in range(table_html.shape[0]):
            table_html.iat[i, 1] = Money(table_html.iat[i, 1], currency)
            table_html.iat[i, 2] = Money(table_html.iat[i, 2], currency)
        return table_html
    except:

        return table_html