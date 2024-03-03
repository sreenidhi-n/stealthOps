import requests
from etherscan import Client

custom_session = requests.Session()
custom_session.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))

es = Client(api_key='RYE29BMTQC3B447KFWDE1GQK9UM7XICDRS') # put your api key here.

es.requests_params = {'session': custom_session}
eth_balance = es.get_eth_balance('0x39eB410144784010b84B076087B073889411F878')
eth_transactions = es.get_transactions_by_address('0x39eB410144784010b84B076087B073889411F878')

print("Ethereum Balance:", eth_balance)

print("\nEthereum Transactions:")
#print(eth_transactions)
for transaction in eth_transactions:
    print(f"Transaction Hash: {transaction['hash']}")
    print(f"From: {transaction['from']}")
    print(f"To: {transaction['to']}")
    print(f"Value: {transaction['value']} wei")
    print(f"Timestamp: {transaction['timestamp']}")
    print()  # Empty line for better readability between transactions
