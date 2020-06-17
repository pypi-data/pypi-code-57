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

    def __init__(self, bank_account, ledger_host, ledger_read_host=None):
        self.bank_account = bank_account
        self.ledger = LedgerClient(ledger_endpoint=ledger_host, ledger_read_only_endpoint=ledger_read_host)

        log.info("---------Initialising-------------")
        log.info(f"Bank Account Number:  {self.bank_account['account_id']}")
        log.info(f"Cash Book:  {self.DEFAULT_CASH_BOOK_ID}")

    def get_book(self):
        log.info("---------Get Book----------")
        blocked_balance_book = self.ledger.get_book(book_id=self.bank_account['ledger_books']['blocked_balance']['id'])['balances']
        main_balance_book = self.ledger.get_book(book_id=self.bank_account['ledger_books']['main_balance']['id'])['balances']
        blocked_balance_deposit_book = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], metadata_filter={'operation': 'DEPOSIT'})
        blocked_balance_withdraw_book = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['blocked_balance']['id'], metadata_filter={'operation': 'WITHDRAW'})
        book_balance = []
        for currency, amount in blocked_balance_book.items():
            if currency in main_balance_book:
                main_balance = main_balance_book[currency]
            else:
                main_balance = "0"
            if currency in blocked_balance_deposit_book:
                blocked_balance_deposit = blocked_balance_deposit_book[currency]
            else:
                blocked_balance_deposit = "0"
            if currency in blocked_balance_withdraw_book:
                blocked_balance_withdraw = blocked_balance_withdraw_book[currency]
            else:
                blocked_balance_withdraw = "0"
            balance = {
                'currency': currency,
                'blocked_balance_deposit': blocked_balance_deposit,
                'blocked_balance_withdraw': blocked_balance_withdraw,
                'main_balance': main_balance
            }
            book_balance.append(dict(balance))
        return book_balance

    def get_book_balances(self, currency: str, metadata_filter: dict = {}):
        log.info("---------Balance----------")
        blocked_deposit_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={**{'operation': 'DEPOSIT'}, **metadata_filter})
        blocked_withdraw_balance = self.ledger.get_book_balances(
            book_id=self.bank_account['ledger_books']['blocked_balance']['id'],
            asset_id=currency, metadata_filter={**{'operation': 'WITHDRAW'}, **metadata_filter})
        main_balance = self.ledger.get_book_balances(book_id=self.bank_account['ledger_books']['main_balance']['id'],
                                                     asset_id=currency, metadata_filter={**metadata_filter})
        return {'currency': currency,
                'blocked_balance_deposit': blocked_deposit_balance.get(currency, "0"),
                'blocked_balance_withdraw': blocked_withdraw_balance.get(currency, "0"),
                'main_balance': main_balance.get(currency, "0")}

    def withdraw_block_amount(self, value: str, currency: str, memo: str, metadata: dict = {}):
        log.info("---------Block_Amount_Withdraw----------")
        operation = self.ledger.post_transfer_sync(
            from_book_id=self.bank_account['ledger_books']['main_balance']['id'],
            to_book_id=self.bank_account['ledger_books']['blocked_balance']['id'], asset_id=currency, value=value,
            memo=memo, metadata={**{"operation": "WITHDRAW"}, **metadata})
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

    def block_trade_amount(self, from_currency: str, to_currency: str, from_amount: str, to_amount: str, memo: str):
        log.info("---------Block_Trade_Amount----------")
        withdraw_block_amount = self.withdraw_block_amount(value=from_amount, currency=from_currency, memo=memo)
        deposit_block_amount = self.deposit_block_amount(value=to_amount, currency=to_currency, memo=memo)
        operation = {
            'withdraw_block_amount': withdraw_block_amount,
            'deposit_block_amount': deposit_block_amount
        }
        log.info(operation)
        return operation

    def trade_amount(self, from_currency: str, to_currency: str, from_amount: str, to_amount: str, memo: str):
        log.info("---------Trade_Amount----------")
        withdraw_amount = self.withdraw_amount(value=from_amount, currency=from_currency, memo=memo)
        deposit_amount = self.deposit_amount(value=to_amount, currency=to_currency, memo=memo)
        operation = {
            'withdraw_block_amount': withdraw_amount,
            'deposit_block_amount': deposit_amount
        }
        log.info(operation)
        return operation

    @staticmethod
    def create_book(account_id: str, ledger_host):
        log.info("---------New_ledger-------------")
        ledger = LedgerClient(ledger_endpoint=ledger_host)
        block_book_id = ledger.create_book(name=f"{account_id}_block_book", min_balance="0")
        main_book_id = ledger.create_book(name=f"{account_id}_main_book", min_balance="0")
        new_books = {
            'main_balance': {'name': main_book_id['name'],
                             'id': main_book_id['id']},
            'blocked_balance': {'name': block_book_id['name'],
                                'id': block_book_id['id']}
        }
        log.info(new_books)
        return new_books
