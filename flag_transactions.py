import requests

base_url = "https://api.chainabuse.com/v1"

api_key = "ca_aUVPWmpENkZwRENPd3RiYVBOTkI3SDhFLnZVSVdSSm1Nem1kQVBMWmVibXh4bFE9PQ"

def address_lookup(address):
    endpoint = f"{base_url}/address/{address}"
    params = {"apikey": api_key}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def analyze_transaction(tx_hash):
    endpoint = f"{base_url}/transaction/{tx_hash}"
    params = {"apikey": api_key}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_risk_score(address):
    data = address_lookup(address)
    if data:
        return data.get("risk_score")
    else:
        return None

def tag_address(address, tag):
    endpoint = f"{base_url}/address/{address}/tag"
    params = {"apikey": api_key}
    payload = {"tag": tag}
    response = requests.post(endpoint, params=params, json=payload)
    return response.status_code

def setup_alerts(address):
    endpoint = f"{base_url}/address/{address}/alerts"
    params = {"apikey": api_key}
    payload = {"enabled": True}
    response = requests.put(endpoint, params=params, json=payload)
    return response.status_code

address = "0x39eB410144784010b84B076087B073889411F878"
tx_hash = "0x123456789abcdef123456789abcdef123456789abcdef123456789abcdef"

address_info = address_lookup(address)
print("Address Lookup Result:", address_info)

tx_info = analyze_transaction(tx_hash)
print("Transaction Analysis Result:", tx_info)

risk_score = get_risk_score(address)
print("Risk Score:", risk_score)

tag_status = tag_address(address, "High Risk")
print("Tagging Status:", tag_status)

alerts_status = setup_alerts(address)
print("Alerts Setup Status:", alerts_status)
