import json

filename = 'Chapter_10/user_info.json'

user_info = {}

user_info['username'] = input("What is your username? ")
user_info['age'] = input("How old are you? ")
user_info['favorite_color'] = input("What is your favorite color? ")

with open(filename, 'w') as file_object:
    json.dump(user_info, file_object)

with open(filename) as file_object:
    saved_info = json.load(file_object)

print("\nHere's what I remember about you:")
print(f"Username: {saved_info['username']}")
print(f"Age: {saved_info['age']}")
print(f"Favorite color: {saved_info['favorite_color']}")