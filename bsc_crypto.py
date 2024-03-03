import requests

base_url = "https://api.bscscan.com/api"

api_key = "7U5WEN3WCPPU5YET42I44RYEQT8UNSYCVF"

address = "0x39eB410144784010b84B076087B073889411F878"

def get_bsc_balance(address):
    endpoint = f"{base_url}?module=account&action=balance&address={address}&apikey={api_key}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data["result"]
    else:
        return None

def get_bsc_transactions(address):
    endpoint = f"{base_url}?module=account&action=txlist&address={address}&apikey={api_key}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data["result"]
    else:
        return None

bsc_balance = get_bsc_balance(address)
bsc_transactions = get_bsc_transactions(address)

print("BSC Balance:", bsc_balance)
print("BSC Transactions:", bsc_transactions)
