filenames = ['Chapter_10/cats.txt', 'Chapter_10/dogs.txt']

for filename in filenames:
    try:
        with open(filename) as file_object:
            contents = file_object.read()
            print(f"\nContents of {filename}:")
            print(contents)

    except FileNotFoundError:
        pass