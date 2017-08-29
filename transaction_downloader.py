from CoinbaseHelper import CoinbaseHelper

import json


# Create the client so we can make requests.
api_key = raw_input('What is your API key?: ')
api_secret = raw_input('What is the secret key?: ')

helper = CoinbaseHelper(api_key, api_secret)

for bt in helper.get_btc_transaction_amounts():
    print 'BITCOIN'
    print json.dumps(bt, indent=4)

for lt in helper.get_ltc_transaction_amounts():
    print 'LITECOIN'
    print json.dumps(lt, indent=4)

for et in helper.get_eth_transaction_amounts():
    print 'ETHERIUM'
    print json.dumps(et, indent=4)