import requests

response = requests.post('http://localhost:5000/api/dict', json={'source': 'es', 'target':'en', 'word': 'hablar'}, timeout=10)
print(response.json())

j={'source': 'es', 'target':'en', 'word': "mujer"}
response = requests.post('http://localhost:5000/api/dict', json=j, timeout=10)
print(response.json())

j={'source': 'es', 'target':'en', 'word': "brazos"}
response = requests.post('http://localhost:5000/api/dict', json=j, timeout=10)
print(response.json())

j={'source': 'es', 'target':'en', 'word': "caliente"}
response = requests.post('http://localhost:5000/api/dict', json=j, timeout=10)
print(response.json())

j={'source': 'it', 'target':'en', 'word': "mezzo"}
response = requests.post('http://localhost:5000/api/dict', json=j, timeout=10)
print(response.json())

j={'source': 'en', 'target':'es', 'word': "backpack"}
response = requests.post('http://localhost:5000/api/dict', json=j, timeout=10)
print(response.json())
