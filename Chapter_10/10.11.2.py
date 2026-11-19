import json

filename = 'Chapter_10/favorite_number.json'

with open(filename) as file_object:
    number = json.load(file_object)

print(f"I know your favorite number! It's {number}.")