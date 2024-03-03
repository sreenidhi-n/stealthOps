import requests

url = "https://api.proxynova.com/comb"
query = input("Enter the query: ")

params = {
    "query": query
}

response = requests.get(url, params=params)
if response.status_code == 200:
    data = response.json()
    lines = data.get("lines", [])
    for line in lines:
        print(line)
else:
    print("Error:", response.status_code)
