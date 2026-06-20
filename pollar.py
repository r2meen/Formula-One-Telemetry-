import requests
import time

url = "https://api.openf1.org/v1/laps"
params = {"session_key": "latest"}
response = requests.get(url, params=params)

last_count = 0

while True:
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        laps = response.json()
        current_count = len(laps)
        
        if current_count > last_count:
            print(f"New laps detected! Now at {current_count} laps (was {last_count})")
        else:
            print(f"No change. Still at {current_count} laps")
        
        last_count = current_count
    else:
        print("Request failed, status code:", response.status_code)
    
    time.sleep(5)