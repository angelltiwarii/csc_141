import json

number = input("What is your favorite number? ")

filename = 'Chapter_10/favorite_number.json'

with open(filename, 'w') as file_object:
    json.dump(number, file_object)

print("Your favorite number has been saved!")