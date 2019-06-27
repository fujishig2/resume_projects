import pickle

filepath = input("Enter a file name [data/trips.txt]: ")
if filepath == "":
    filepath = r"C:\Users\User\Downloads\CMPT 103\Project\data\trips.txt"
trips_file = open(filepath)
line = trips_file.readline()
line = trips_file.readline()
IDs = {}
while line != "":
    temp = line.split(",")
    if temp[0] not in IDs:
        IDs[temp[0]] = set([temp[-1].strip()])
    else:
        IDs[temp[0]].add(temp[-1].strip())
    line = trips_file.readline()
trips_file.close()









file = open(r"C:\Users\User\Downloads\CMPT 103\awesome.txt", "x+b")
pickle.dump(IDs, file)
file.close
file = open(r"C:\Users\User\Downloads\CMPT 103\awesome.txt", "r+b")
s= pickle.load(file)
file.close()
print(s)