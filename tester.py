import requests

print(f"Valid, check all entries.")
print(requests.get("http://127.0.0.1:5000/").json())

print("Adding an item:")
print(requests.post("http://127.0.0.1:5000/", json={"name": "Dill", "size": 1, "juiciness": 1, "description": "", "id": 3},).json())

print("Valid, get an entry.")
print(requests.get("http://127.0.0.1:5000/fruit/1").json())

print("Updating an item:")
print(requests.get("http://127.0.0.1:5000/fruit/0").json())
# print(requests.put("http://127.0.0.1:5000/update/0?juiciness=2").json())
print(requests.get("http://127.0.0.1:5000/fruit/0").json())
print("Update complete")

print("Get an invalid entry.")
print(requests.get("http://127.0.0.1:5000/fruit/8").json())

print("Deleting an time:")
print(requests.delete("http://127.0.0.1:50000/delete/0"))
print(requests.get("http://127.0.0.1:5000/").json())
