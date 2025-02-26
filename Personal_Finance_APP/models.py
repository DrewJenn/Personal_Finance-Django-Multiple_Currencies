from django.db import models
from django.contrib.auth.models import User
from djmoney.models.fields import MoneyField
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from moneyed import Money



class BankAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bank_accounts", db_index=True)
    account_holder_name = models.CharField(max_length=25, blank=False)      
    bank_name = models.CharField(max_length=100, blank=False)
    account_type = models.CharField(max_length=25, blank=False)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    compound_interest = models.BooleanField(default=False)
    compound_interest_frequency = models.CharField(null=True, max_length=15)
    interest_payout_frequency = models.CharField(null=True, max_length=20)
    account_id = models.PositiveIntegerField(default=1)  
    account_balance = MoneyField(null=True, max_digits=10, decimal_places=2, default_currency='USD', db_index=True)
    

    initial_account_date = models.DateField(null=True)
    initial_account_balance = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency='USD')


    def activate_account(self):
        self.initial_account_balance = self.account_balance
        self.initial_account_date = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.account_id:
            last_account = BankAccount.objects.order_by('-account_id').first()
            self.account_id = last_account.account_id + 1 if last_account else 1
        super().save(*args, **kwargs)    

    def get_currency(self):
        return str(self.account_balance.currency)
    
    def get_amount(self):
        return self.account_balance.amount
    
    def get_initial_amount(self):
        return self.initial_account_balance.amount

    def process_deposit(self, amount):
        if amount <= 0:
            return False
        self.account_balance += Money(amount, self.account_balance.currency)
        self.save()
        print(f"Balance after deposit: {self.account_balance}")
        return True
    
    def process_withdrawal(self, amount):
        control = Money(0.00, self.account_balance.currency)
        if amount <= 0 or (self.account_balance - Money(amount, self.account_balance.currency)) < control:
            return False
        self.account_balance -= Money(amount, self.account_balance.currency)
        self.save()
        print(f"Balance after withdrawal: {self.account_balance}")
        return True



class BankRecord(models.Model):
    account_id = models.ForeignKey(BankAccount, on_delete=models.SET_NULL, related_name='bank_records', null=True, db_index=True)
    deposit_record = models.BooleanField(default=False)
    withdrawal_record = models.BooleanField(default=False)
    transaction_amount = MoneyField(null=True, max_digits=10, decimal_places=2, default_currency='USD')
    transaction_date = models.DateField(default=timezone.now)


    new_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True) # adds balance to account record for easier graphing



    uninitialized_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  #temp input

    def get_transaction_amount(self):
        return self.transaction_amount.amount
    
    def get_transaction_currency(self):
        self.transaction_amount.currency

@receiver(pre_save, sender=BankRecord)
def set_transaction_amount_currency(sender, instance, **kwargs):
    instance.transaction_amount = Money(instance.uninitialized_amount, instance.account_id.get_currency())    
