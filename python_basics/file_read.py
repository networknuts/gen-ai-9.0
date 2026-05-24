file_path = input("Enter the file path: ")

f = open(file_path,"r")

for line in f.readlines():
    print(line.strip())

f.close()