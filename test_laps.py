import requests

url = "https://api.openf1.org/v1/laps"
params = {"session_key": "latest"}

response = requests.get(url, params=params)

print("Status code:", response.status_code)
print(response.json()[:3])