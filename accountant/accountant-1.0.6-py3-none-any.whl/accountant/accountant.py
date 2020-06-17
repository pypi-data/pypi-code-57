from ledger.client import LedgerClient

import logging

log = logging.getLogger(__name__)


class Accountant:
    """
    Accountant binds together 2 concepts - BankAccount & Ledger
    Ledger is the source of truth for the Bank
    Ledger ALWAYS reflect the true state of the OutsideWorld
    Accountant MUST manage BankAccount's books inside Ledger properly
    Accountant stores no state
    """
    DEFAULT_CASH_BOOK_ID = {'name': 'cash_book', 'id': '1'}

    def __init__(self, bank_account):
        self.bank_account = bank_account
        self.ledger = LedgerClient(ledger_host="http://ledger-service-dev-1.local-dev:3000/")

        log.info("---------Initialising-------------")
        log.info("Bank Account Number: ", self.bank_account['account_id'])
        log.info("Cash Book: ", self.DEFAULT_CASH_BOOK_ID)

    def get_book(self):
        log.info("---------Get Book----------")
        blocked_balance_book = self.ledger.get_book(book_id=self.bank_account['ledger_books']['blocked_balance']['id'])['balances']
        main_balance_book = self.ledger.get_book(book_id=self.bank_account['ledger_books']['main_balance']['id'])['balances']
        blocked_balance_deposit_book = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], metadata_filter={'operation': 'DEPOSIT'})
        blocked_balance_withdraw_book = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], metadata_filter={'operation': 'WITHDRAW'})
        book_balance = []
        for currency, amount in blocked_balance_book.items():
            if currency in main_balance_book:
                main_balance = float(main_balance_book[currency])
            else:
                main_balance = float(0)
            if currency in blocked_balance_deposit_book:
                blocked_balance_deposit = float(blocked_balance_deposit_book[currency])
            else:
                blocked_balance_deposit = float(0)
            if currency in blocked_balance_withdraw_book:
                blocked_balance_withdraw = float(blocked_balance_withdraw_book[currency])
            else:
                blocked_balance_withdraw = float(0)
            balance = {
                'currency': currency,
                'blocked_balance_deposit': blocked_balance_deposit,
                'blocked_balance_withdraw': blocked_balance_withdraw,
                'main_balance': main_balance
            }
            book_balance.append(dict(balance))
        return book_balance

    def get_book_balances(self, currency: str):
        log.info("---------Balance----------")
        blocked_deposit_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={'operation': 'DEPOSIT'})

        blocked_withdraw_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={'operation': 'WITHDRAW'})

        main_balance = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['main_balance']['id'],
                                                     asset_id=currency)

        return {'currency': currency,
                'blocked_balance_deposit': float(blocked_deposit_balance[currency]),
                'blocked_balance_withdraw': float(blocked_withdraw_balance[currency]),
                'main_balance': float(main_balance[currency])}

    def withdraw_block_amount(self, value: str, currency: str, memo: str):
        log.info("---------Block_Amount_Withdraw----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['main_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'], asset_id=currency, value=value,
            memo=memo, metadata={'operation': 'WITHDRAW'})
        log.info(operation)
        return operation

    def deposit_block_amount(self, value: str, currency: str, memo: str):
        log.info("---------Block_Amount_Deposit----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.DEFAULT_CASH_BOOK_ID['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'], asset_id=currency, value=value,
            memo=memo,
            metadata={'operation': 'DEPOSIT'})
        log.info(operation)
        return operation

    def withdraw_unblock_amount(self, value: str, currency: str, memo: str):
        log.info("---------Unblock_Amount_Withdraw----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['main_balance']['id'], asset_id=currency, value=value,
            memo=memo,
            metadata={'operation': 'WITHDRAW'})
        log.info(operation)
        return operation

    def deposit_unblock_amount(self, value: str, currency: str, memo: str):
        log.info("---------Unblock_Amount_Deposit----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.DEFAULT_CASH_BOOK_ID['id'], asset_id=currency, value=value, memo=memo,
            metadata={'operation': 'DEPOSIT'})
        log.info(operation)
        return operation

    def withdraw_amount(self, value: str, currency: str, memo: str):
        log.info("---------Withdraw_amount----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.DEFAULT_CASH_BOOK_ID['id'],
            asset_id=currency, value=value, memo=memo, metadata={'operation': 'WITHDRAW'})
        log.info(operation)
        return operation

    def deposit_amount(self, value: str, currency: str, memo: str):
        log.info("---------Deposit_amount----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            to_book_id=self.bank_account['ledger_books'][
                'main_balance']['id'], asset_id=currency, value=value,
            memo=memo, metadata={'operation': 'DEPOSIT'})
        log.info(operation)
        return operation

    @staticmethod
    def create_book(account_id: str):
        log.info("---------New_ledger-------------")
        ledger = LedgerClient(ledger_host="http://ledger-service-dev-1.local-dev:3000/")
        block_book_id = ledger.create_book(name=f"{account_id}_block_book",
                                                min_balance="-100")
        main_book_id = ledger.create_book(name=f"{account_id}_main_book", min_balance="-100")
        new_books = {
            'main_balance': {'name': main_book_id['name'],
                             'id': main_book_id['id']},
            'blocked_balance': {'name': block_book_id['name'],
                                'id': block_book_id['id']}
        }
        log.info(new_books)
        return new_books

