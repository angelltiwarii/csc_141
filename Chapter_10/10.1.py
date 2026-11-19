10.1
filename = 'Chapter_10/learning_python.txt'

# Reading the entire file
with open(filename) as file_object:
    contents = file_object.read()
    print(contents)

# Reading lines into a list
with open(filename) as file_object:
    lines = file_object.readlines()

for line in lines:
    print(line.rstrip())