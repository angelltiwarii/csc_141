filename = 'Chapter_10/learning_python.txt'

with open(filename) as file_object:
    contents = file_object.read()

for line in contents.splitlines():
    print(line)