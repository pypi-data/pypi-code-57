import json

class Transaction:
    def __init__(self, id, type, document_id, transaction_number,
                 transaction_date, general_ledger, book_year, period, description, total_amount, currency, is_final):
        self.id = id
        self.type = type
        self.document_id = document_id
        self.transaction_number = transaction_number
        self.transaction_date = transaction_date
        self.general_ledger = general_ledger
        self.book_year = book_year
        self.period = period
        self.description = description
        self.total_amount = total_amount
        self.currency = currency
        self.is_final = is_final
        self.artifacts = None

    @classmethod
    def from_dict(cls, data):
        """
        Create Transaction instance from API response data
        """
        currency = data.get('currency')
        currency = currency['code'] if currency else None

        return cls(
            id = data['transactionId'],
            type = data['type'],
            document_id = data['documentId'],
            transaction_number = data['transactionNumber'],
            transaction_date = data['transactionDate'],
            general_ledger = data['generalLedger']['code'],
            book_year = data['bookYear'],
            period = data['period'],
            description = data.get('description'),
            total_amount= data.get('totalAmount'),
            currency = currency,
            is_final = data['isFinalBooking']
        )

    def to_json(self):
        return dict(
            id = self.id,
            type = self.type,
            document_id = self.document_id,
            transaction_number = self.transaction_number,
            transaction_date = self.transaction_date,
            general_ledger = self.general_ledger,
            book_year = self.book_year,
            period = self.period,
            description = self.description, 
            total_amount = self.total_amount,
            currency = self.currency,
            is_final = self.is_final
        )