from moneyed import Money
import pandas as pd
import yfinance as yf
from Personal_Finance_APP.models import BankAccount






def home_get_total_balance(df):
    df['total_named_balance'] = pd.to_numeric(df['total_named_balance'], errors='coerce')
    df['total_named_balance'] = df['total_named_balance'].round(2)
    test_USD = df.copy()

    for i in range (df.shape[0]):
        if df.iat[i, 0] != 'USD':
            exchange_rate = get_exchange_rate(df.iat[i, 0], 'USD')
            test_USD.iat[i, 1] = (test_USD.iat[i, 1] * exchange_rate).round(2)

    test_USD = test_USD.sort_values(by='total_named_balance', ascending=False)
    conversion_currency = test_USD.iat[0, 0]
    for i in range(df.shape[0]):
        conversion_rate = get_exchange_rate(df.iat[i, 0], conversion_currency)
        if conversion_rate:
            df.iat[i, 1] = (df.iat[i, 1] * conversion_rate)
    return (Money(df.total_named_balance.sum(), conversion_currency), conversion_currency)




def get_exchange_rate(base_currency, target_currency):
    ticker_symbol = f"{base_currency}{target_currency}=X"
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d") 
        exchange_rate = data['Close'].iloc[-1] 
        return exchange_rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        answer = secondary_get_exchange_rate(base_currency, target_currency)
        if answer:
            return answer
        else:
            return None  
        
def secondary_get_exchange_rate(base_currency, target_currency):
    base_to_usd = extra_get_exchange_rate(base_currency, "USD")
    target_to_usd = extra_get_exchange_rate(target_currency, "USD")
    try:
        answer = (base_to_usd / target_to_usd)
        return answer
    except:
        return None

def extra_get_exchange_rate(base_currency, target_currency):
    ticker_symbol = f"{base_currency}{target_currency}=X"
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d") 
        exchange_rate = data['Close'].iloc[-1] 
        return exchange_rate
    except Exception as e:
        print(f"Error fetching exchange rate: {e}")
        return None

def get_selected_account(user, account_id):
    if user.bank_accounts.exists():
        if account_id:
            return BankAccount.objects.get(id=account_id, user=user)
        return user.bank_accounts.first()  
    return None

