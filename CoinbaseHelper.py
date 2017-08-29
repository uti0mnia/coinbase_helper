from coinbase.wallet.client import Client
import coinbase.wallet.error as CBErrors

import json

litecoin = 'LTC'
bitcoin = 'BTC'
etherium = 'ETH'

class CoinbaseHelper:
    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

        try:
            self.accounts = self.client.get_accounts()
        except CBErrors.AuthenticationError:
            raise Exception('Authentication error. You sure you have the right API key/secret?')

    # ACCOUNTS
    def get_accounts(self, currency):
        """ Returns the user's accounts for a given currency (Bitcoin, Litecoin or Etherium)."""

        if currency is None:
            return []

        if self.accounts is None:
            print 'No accounts associated with helper.'
            return []

        return filter(lambda data: data['currency'] == currency, self.accounts['data'])

    def get_btc_accounts(self):
        """ Returns the user's bitcoin accounts."""
        return self.get_accounts(bitcoin)

    def get_ltc_accounts(self):
        """ Returns the user's litecoin accounts."""
        return self.get_accounts(litecoin)

    def get_eth_accounts(self):
        """ Returns the user's etherium accounts"""
        return self.get_accounts(etherium)

    # TRANSACTIONS
    def get_transactions(self, currency):
        """ Return all transactions for a currency (Bitcoin, Litecoin, Etherium)."""
        if currency is None:
            return []

        transactions = []
        for account in self.get_accounts(currency):
            try:
                transactions += self.client.get_transactions(account['id'])['data']
            except:
                print 'Cannot get transactions'

        return transactions

    def get_btc_transactions(self):
        """ Returns all the bitcoin transactions."""
        return self.get_transactions(bitcoin)

    def get_ltc_transactions(self):
        """ Returns all the litecoin transactions."""
        return self.get_transactions(litecoin)

    def get_eth_transactions(self):
        """ Returns all the etherium transactions."""
        return self.get_transactions(etherium)

    def get_all_transactions(self):
        """ Returns all transactions for the user."""
        transactions = self.get_btc_transactions()
        transactions += self.get_ltc_accounts()
        transactions += self.get_eth_accounts()

        return transactions

    def get_transaction_amounts(self, currency):
        """ Returns the cost per coin, amount of the coin purchased, the cost and the curreny purchased in for a
            given currency (Bitcoin, Litecoin, Etherium)."""
        if currency is None:
            return []

        transactions = []
        for transaction in self.get_transactions(currency):
            if transaction['status'] != 'completed':
                continue

            amount = float(transaction['amount']['amount'])
            cost = float(transaction['native_amount']['amount'])
            native_currency = transaction['native_amount']['currency']
            cost_per_coin = cost/amount
            date = transaction['updated_at']

            transactions.append({
                'amount': amount,
                'cost': cost,
                'native_currency': native_currency,
                'cost_per_coin': cost_per_coin,
                'date': date
            })

        return transactions

    def get_btc_transaction_amounts(self):
        """ Returns get_transaction_amounts() for bitcoin."""
        return self.get_transaction_amounts(bitcoin)

    def get_ltc_transaction_amounts(self):
        """ Returns get_transaction_amounts() for litecoin."""
        return self.get_transaction_amounts(litecoin)

    def get_eth_transaction_amounts(self):
        """ Returns get_transaction_amounts() for etherium."""
        return self.get_transaction_amounts(etherium)
