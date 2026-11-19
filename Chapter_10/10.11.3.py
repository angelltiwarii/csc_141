import json

filename = 'Chapter_10/favorite_number.json'

try:
    with open(filename) as file_object:
        number = json.load(file_object)

except FileNotFoundError:
    number = input("What is your favorite number? ")

    with open(filename, 'w') as file_object:
        json.dump(number, file_object)

    print("Your favorite number has been saved!")

else:
    print(f"I know your favorite number! It's {number}.")