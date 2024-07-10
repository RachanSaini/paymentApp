# bank_simulator.py
import random

class BankSimulator:
    @staticmethod
    def validate_card(card_number, expiry_month, expiry_year, cvv):
        # Simple validation logic for card details
        if len(str(card_number)) != 16:
            return False
        if not (1 <= int(expiry_month) <= 12):
            return False
        if len(str(expiry_year)) != 4:
            return False
        if len(str(cvv)) != 3:
            return False
        return True

    @staticmethod
    def process_payment(amount):
        # Simulate payment processing with always true for now
        return True

def simulate_bank_process(payment):
    if not BankSimulator.validate_card(payment.card_number, payment.expiry_month, payment.expiry_year, payment.cvv):
        return False
    return BankSimulator.process_payment(payment.amount)
