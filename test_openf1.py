import requests

# This endpoint gets the most recent F1 sessions (practice, qualifying, race, etc.)
url = "https://api.openf1.org/v1/sessions"
params = {"year": 2025}  # adjust to whatever year has recent data

response = requests.get(url, params=params)

print("Status code:", response.status_code)
print(response.json()[:3])  # just print the first 3 results so it's not a wall of text