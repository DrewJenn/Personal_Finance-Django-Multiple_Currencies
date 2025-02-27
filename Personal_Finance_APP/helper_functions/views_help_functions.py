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

def get_exchange_rate(base_currency, target_currency, check = 0):
    if base_currency == target_currency:
        return 1
    ticker_symbol = f"{base_currency}{target_currency}=X"
    cached_rate = cache.get(ticker_symbol)
    if cached_rate:
        return cached_rate
    try:
        ticker = yf.Ticker(ticker_symbol)
        data = ticker.history(period="1d") 
        exchange_rate = data['Close'].iloc[-1] 
        cache.set(ticker_symbol, exchange_rate, timeout=1800)
        return exchange_rate
    except:
        if check == 0:
            try:
                answer = secondary_get_exchange_rate(base_currency, target_currency)
            except Exception as secondary_error:
                print(f"Error in secondary method: {secondary_error}")
                answer = None
        else:
            answer = None
        if answer:
            cache.set(ticker_symbol, answer, timeout=1800)
        return answer
        
def secondary_get_exchange_rate(base_currency, target_currency):
    try:
        return(get_exchange_rate(base_currency, "USD", 1) / get_exchange_rate(target_currency, "USD", 1))
    except:
        return None

def get_selected_account(user, account_id):
    if user.bank_accounts.exists():
        if account_id:
            return BankAccount.objects.get(id=account_id, user=user)
        return user.bank_accounts.first()  
    return None

def get_real_time_stock_price(ticker: str) -> float:
    try:
        ticker_yahoo = yf.Ticker(ticker)
        data = ticker_yahoo.history()
        last_quote = data['Close'].iloc[-1]
        return last_quote
    except KeyError:
        print(f"Error: Unable to fetch real-time data for {ticker}. Maybe the ticker is invalid.")
        return None
    except Exception as e:
        print(f"Error retrieving data for {ticker}: {e}")
        return None
