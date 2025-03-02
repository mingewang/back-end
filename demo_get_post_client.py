import requests
import json

url = "http://127.0.0.1:5000/get_example"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    print("User Data:", data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

#post
url = "http://127.0.0.1:5000/post_example"
# Data to send in POST request (send as JSON)
data = {"name": "test", "age": 11}
# Send the POST request with 'json' argument (requests will automatically convert it to JSON)
response = requests.post(url, json=data)

if response.status_code == 200:
    data = response.json()
    print("Post request, get response User Data:", data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

