name = input("What is your name? ")

filename = 'Chapter_10/guest.txt'

with open(filename, 'w') as file_object:
    file_object.write(name)

print(f"Hello, {name}! Your name has been saved.")