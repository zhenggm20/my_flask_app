import requests
import json

url = 'http://127.0.0.1:5000/tasks'
headers = {'Content-Type': 'application/json'}
data = {
    "title": "Buy groceries",
    "description": "Get milk and bread",
    "due_date": "2024-09-15T10:00:00"
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print("Response:", response.json())