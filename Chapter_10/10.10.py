filenames = ['Chapter_10/alice.txt']

for filename in filenames:
    try:
        with open(filename, encoding='utf-8') as file_object:
            contents = file_object.read()

    except FileNotFoundError:
        print(f"The file {filename} was not found.")

    else:
        words = contents.lower().count('the')
        words_with_space = contents.lower().count('the ')

        print(f"\nFile: {filename}")
        print(f"Occurrences of 'the': {words}")
        print(f"Occurrences of 'the ': {words_with_space}")