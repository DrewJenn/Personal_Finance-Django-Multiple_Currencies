import threading
import time
from django.core.management.base import BaseCommand
from Personal_Finance_APP.helper_functions import views_help_functions as helper

threshold = 1e-10

CURRENCIES = ('AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN',
              'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLF',
              'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN',
              'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HTG',
              'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF',
              'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA',
              'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MXV', 'MYR', 'MZN', 'NAD', 'NGN',
              'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON',
              'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLE', 'SLL', 'SOS', 'SRD',
              'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD',
              'TZS', 'UAH', 'UGX', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD',
              'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW')

stock_tickers = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'NFLX', 'BA', 'V', 
    'MA', 'DIS', 'INTC', 'IBM', 'PYPL', 'CSCO', 'PFE', 'JNJ', 'KO', 'PEP', 'WMT', 
    'GOOG', 'BABA', 'AMD', 'T', 'CVX', 'XOM', 'GM', 'F', 'SNAP', 'SPY', 'QQQ', 
    'VTI', 'JPM', 'GS', 'BLK', 'MS', 'LUV', 'UAL', 'AAL', 'SPG', 'HPE', 'DELL', 
    'ORCL', 'CRM', 'WFC', 'GS', 'LMT']

class Command(BaseCommand):
    help = 'Updates exchange rates to USD every 5 minutes and prints the updated rates.'

    def handle(self, *args, **kwargs):
        self.print_exchange_rates_in_background()

    def print_exchange_rates_in_background(self):
        def update_exchange_rates():
            while True:
                updated_rates = {}
                for currency in CURRENCIES:
                    try:
                        rate = helper.get_exchange_rate(currency, 'USD')  
                        if rate:
                            updated_rates[currency] = rate
                    except Exception as e:
                        self.stdout.write(f"Error getting exchange rate for {currency}: {e}")
                stock_AAPL = helper.get_real_time_stock_price('AAPL')
                print(stock_AAPL)
                foreign_price = {}
                for currency, rate in updated_rates.items():
                    foreign_price[currency] = (stock_AAPL / rate)
                final_price = {}
                for foreign_currency, price in foreign_price.items():
                    answer = price * helper.get_exchange_rate(foreign_currency, "USD") - stock_AAPL
                    if abs(answer) < threshold:
                        answer = 0.0
                    final_price[foreign_currency + " : " + str(stock_AAPL) + " USD"] = str(answer) + " USD"
                for price in final_price.items():
                    print(), print(price), print()
                time.sleep(60)  

        exchange_rate_thread = threading.Thread(target=update_exchange_rates, daemon=True)
        exchange_rate_thread.start()
        time.sleep(3600)
