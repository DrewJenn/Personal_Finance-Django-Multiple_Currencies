from django.core.management.base import BaseCommand 
import pandas as pd
from django.db import transaction
from moneyed import Money
from datetime import date
from Personal_Finance_APP.models import BankAccount, User, BankRecord

class Command(BaseCommand):
    help = 'Loads data into the database'

    def add_arguments(self, parser):
        parser.add_argument("--file", type=str, help="File Path")
        parser.add_argument("--username", type=str, help="Username")
        parser.add_argument("--password", type=str, help="Password")
        parser.add_argument("--firstName", type=str, help="First Name")
        parser.add_argument("--lastName", type=str, help="Last Name")
        parser.add_argument("--email", type=str, help="Email")

    def handle(self, *args, **kwargs):
        file = kwargs.get("file")
        username = kwargs.get("username")
        password = kwargs.get("password")
        firstName = kwargs.get("firstName")
        lastName = kwargs.get("lastName")
        email = kwargs.get("email")  

        try:
            create_account_data = pd.read_excel(file, sheet_name=0)  
            create_record_data = pd.read_excel(file, sheet_name=2)

            transactions, transaction_date, initial_balances, deposit, withdraw = [], [], [], [], []

            for i in range(create_account_data.shape[0]):
                current_row = i
                amount, date_list, deposit_record, withdrawal_record = [], [], [], []
                initial_account_balance = create_account_data.iat[current_row, 3]

                for j in range(create_record_data.shape[0]):
                    if (
                        create_record_data.iat[j, 4] == create_account_data.iat[current_row, 0]
                        and create_record_data.iat[j, 5] == create_account_data.iat[current_row, 1]
                        and create_account_data.iat[current_row, 2] == create_record_data.iat[j, 6]
                    ):
                        amount.append(create_record_data.iat[j, 3])
                        date_list.append(create_record_data.iat[j, 0])
                        if create_record_data.iat[j, 1] == 'Y':
                            initial_account_balance -= create_record_data.iat[j, 3]
                            deposit_record.append(True)
                            withdrawal_record.append(False)
                        else: 
                            initial_account_balance += create_record_data.iat[j, 3]
                            withdrawal_record.append(True)
                            deposit_record.append(False)

                initial_balances.append(round(initial_account_balance, 2))
                transaction_date.append(date_list)
                transactions.append(amount)
                deposit.append(deposit_record)
                withdraw.append(withdrawal_record)

            new_balances = []
            for i in range(len(initial_balances)):
                temp_new_balances, account_initial_balance, active_transactions, active_deposit = [], initial_balances[i], transactions[i], deposit[i]
                for j in range(len(active_transactions)):
                    if active_deposit[j]:
                        account_initial_balance += active_transactions[j]
                    else:
                        account_initial_balance -= active_transactions[j]
                    temp_new_balances.append(round(account_initial_balance, 2))
                new_balances.append(temp_new_balances)

        except Exception as e:
            self.stderr.write(f"Error loading fixture: {str(e)}")
            return  

        try:
            with transaction.atomic():
                try:
                    user = User.objects.get(username=username)
                    user.delete()
                    self.stdout.write(f"Existing user {username} deleted.")
                except User.DoesNotExist:
                    self.stdout.write(f"User {username} does not exist, creating new one.")

                user = User.objects.create(
                    username=username,
                    firstName=firstName, 
                    lastName=lastName,
                    email=email,
                )
                user.set_password(password)  # Ensures password is hashed
                user.save()

                list_banks = []
                for i in range(create_account_data.shape[0]):
                    compound_interest = create_account_data.iat[i, 5] == 'Y'

                    bank_account = BankAccount.objects.create(
                        user=user,
                        account_holder_name=create_account_data.iat[i, 0],
                        bank_name=create_account_data.iat[i, 1],
                        account_type=create_account_data.iat[i, 2],
                        interest_rate=create_account_data.iat[i, 4],
                        compound_interest=compound_interest,
                        compound_interest_frequency=create_account_data.iat[i, 6],
                        interest_payout_frequency=create_account_data.iat[i, 7],
                        account_balance=Money(create_account_data.iat[i, 3], 'USD'),
                        initial_account_date=date(2024, 10, 1),
                        initial_account_balance=initial_balances[i],
                    )
                    list_banks.append(bank_account)

                for i in range(len(list_banks)):
                    active_transactions, active_dates, active_deposit, active_withdraw, active_new_balances = transactions[i], transaction_date[i], deposit[i], withdraw[i], new_balances[i]

                    if active_transactions:
                        for j in range(len(active_transactions)):
                            BankRecord.objects.create(
                                account_id=list_banks[i],  
                                deposit_record=active_deposit[j],
                                withdrawal_record=active_withdraw[j],
                                transaction_amount=Money(active_transactions[j], 'USD'),
                                transaction_date=pd.to_datetime(active_dates[j], errors='coerce'),    
                                new_balance=active_new_balances[j],
                                uninitialized_amount=active_transactions[j],
                            )

        except Exception as e:
            self.stderr.write(f"Error loading second fixture: {str(e)}")
