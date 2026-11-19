filename = 'Chapter_10/guest_book.txt'

while True:
    name = input("Enter your name (or 'quit' to exit): ")

    if name == 'quit':
        break

    print(f"Hello, {name}!")

    with open(filename, 'a') as file_object:
        file_object.write(name + '\n')