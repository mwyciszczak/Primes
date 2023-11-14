import requests

url = "http://localhost:8000/returned"

data = {"returned_primes": [22, 23]}

response = requests.post(url, json=data)

if response.status_code == 200:
    returned_data = response.json()
    print("Response:", returned_data)
else:
    print("Request failed with status code:", response.status_code)