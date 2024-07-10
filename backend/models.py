class Payment:
    def __init__(self, payment_id, merchant_id, card_number, expiry_month, expiry_year, amount, currency, cvv, status):
        self.payment_id = payment_id
        self.merchant_id = merchant_id
        self.card_number = card_number
        self.expiry_month = expiry_month
        self.expiry_year = expiry_year
        self.amount = amount
        self.currency = currency
        self.cvv = cvv
        self.status = status
        self.masked_card_number = self.mask_card_number()

    def mask_card_number(self):
        return f"{self.card_number[:4]} **** **** {self.card_number[-4:]}"
